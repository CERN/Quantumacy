# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""AggregatorGRPCServer module."""
import http.client
import json
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from multiprocessing import cpu_count
from time import sleep

from cryptography.fernet import Fernet
from grpc import server
from grpc import ssl_server_credentials

from openfl.protocols import Acknowledgement
from openfl.protocols import add_AggregatorServicer_to_server
from openfl.protocols import AggregatorServicer
from openfl.protocols import MessageHeader
from openfl.protocols import TaskResults
from openfl.protocols import TaskResultsQKD
from openfl.protocols import TasksResponse
from openfl.protocols import TasksResponseQKD
from openfl.protocols import TensorResponse
from openfl.protocols import TensorResponseQKD
from openfl.protocols import NamedTensor
from openfl.protocols import MetadataProto
from openfl.protocols import utils
from openfl.utilities import check_equal
from openfl.utilities import check_is_in
from openfl.protocols.utils import encrypt_AES
from openfl.protocols.utils import decrypt_AES
from openfl.protocols.utils import decrypt_named_tensor
from openfl.protocols.utils import encrypt_named_tensor


class AggregatorGRPCServer(AggregatorServicer):
    """gRPC server class for the Aggregator."""

    def __init__(self,
                 aggregator,
                 agg_port,
                 tls=True,
                 disable_client_auth=False,
                 root_certificate=None,
                 certificate=None,
                 private_key=None,
                 **kwargs):
        """
        Class initializer.

        Args:
            aggregator: The aggregator
        Args:
            fltask (FLtask): The gRPC service task.
            tls (bool): To disable the TLS. (Default: True)
            disable_client_auth (bool): To disable the client side
            authentication. (Default: False)
            root_certificate (str): File path to the CA certificate.
            certificate (str): File path to the server certificate.
            private_key (str): File path to the private key.
            kwargs (dict): Additional arguments to pass into function
        """
        self.aggregator = aggregator
        self.uri = f'[::]:{agg_port}'
        self.tls = tls
        self.disable_client_auth = disable_client_auth
        self.root_certificate = root_certificate
        self.certificate = certificate
        self.private_key = private_key
        self.channel_options = [
            ('grpc.max_metadata_size', 32 * 1024 * 1024),
            ('grpc.max_send_message_length', 128 * 1024 * 1024),
            ('grpc.max_receive_message_length', 128 * 1024 * 1024)
        ]
        self.server = None
        self.server_credentials = None

        self.logger = getLogger(__name__)

        # qkd
        self.cyphers = {}
        self.qkd = True

    def validate_collaborator(self, request, context):
        """
        Validate the collaborator.

        Args:
            request: The gRPC message request
            context: The gRPC context

        Raises:
            ValueError: If the collaborator or collaborator certificate is not
             valid then raises error.

        """
        if self.tls:
            common_name = context.auth_context()[
                'x509_common_name'][0].decode('utf-8')
            collaborator_common_name = request.header.sender
            if not self.aggregator.valid_collaborator_cn_and_id(
                    common_name, collaborator_common_name):
                raise ValueError(
                    f'Invalid collaborator. CN: |{common_name}| '
                    f'collaborator_common_name: |{collaborator_common_name}|')

    def get_header(self, collaborator_name):
        """
        Compose and return MessageHeader.

        Args:
            collaborator_name : str
                The collaborator the message is intended for
        """
        return MessageHeader(
            sender=self.aggregator.uuid,
            receiver=collaborator_name,
            federation_uuid=self.aggregator.federation_uuid,
            single_col_cert_common_name=self.aggregator.single_col_cert_common_name
        )

    def check_request(self, request):
        """
        Validate request header matches expected values.

        Args:
            request : protobuf
                Request sent from a collaborator that requires validation
        """
        # TODO improve this check. the sender name could be spoofed
        check_is_in(request.header.sender, self.aggregator.authorized_cols, self.logger)

        # check that the message is for me
        check_equal(request.header.receiver, self.aggregator.uuid, self.logger)

        # check that the message is for my federation
        check_equal(
            request.header.federation_uuid, self.aggregator.federation_uuid, self.logger)

        # check that we agree on the single cert common name
        check_equal(
            request.header.single_col_cert_common_name,
            self.aggregator.single_col_cert_common_name,
            self.logger
        )

    def GetKey(self, request, context):
        self.validate_collaborator(request, context)
        self.check_request(request)
        collaborator_name = request.header.sender
        if collaborator_name not in self.cyphers:
            self.logger.info('getting key')
            key = self.get_key()
            self.logger.info(key)
            self.cyphers[collaborator_name] = Fernet(key.encode())
        return Acknowledgement(header=self.get_header(collaborator_name))

    def GetTasks(self, request, context):  # NOQA:N802
        """
        Request a job from aggregator.

        Args:
            request: The gRPC message request
            context: The gRPC context

        """
        self.validate_collaborator(request, context)
        self.check_request(request)
        collaborator_name = request.header.sender
        tasks, round_number, sleep_time, time_to_quit = self.aggregator.get_tasks(
            request.header.sender)

        return TasksResponse(
            header=self.get_header(collaborator_name),
            round_number=round_number,
            tasks=tasks,
            sleep_time=sleep_time,
            quit=time_to_quit
        )

    def GetTasksQKD(self, request, context):
        self.validate_collaborator(request, context)
        self.check_request(request)
        collaborator_name = request.header.sender
        tasks, round_number, sleep_time, time_to_quit = self.aggregator.get_tasks(
            request.header.sender)
        header = self.get_header(collaborator_name)

        class Payload:
            def __init__(self):
                self.round_number = round_number
                self.tasks = tasks
                self.sleep_time = sleep_time
                self.quit = time_to_quit

        payload = encrypt_AES(self.cyphers[collaborator_name], Payload())
        return TasksResponseQKD(header=header, payload=payload)

    def GetAggregatedTensor(self, request, context):  # NOQA:N802
        """
        Request a job from aggregator.

        Args:
            request: The gRPC message request
            context: The gRPC context

        """
        self.validate_collaborator(request, context)
        self.check_request(request)
        collaborator_name = request.header.sender
        tensor_name = request.tensor_name
        require_lossless = request.require_lossless
        round_number = request.round_number
        report = request.report
        tags = request.tags

        named_tensor = self.aggregator.get_aggregated_tensor(
            collaborator_name, tensor_name, round_number, report, tags, require_lossless)

        return TensorResponse(header=self.get_header(collaborator_name),
                              round_number=round_number,
                              tensor=named_tensor)

    def GetAggregatedTensorQKD(self, request, context):  # NOQA:N802
        """
        Request a job from aggregator.

        Args:
            request: The gRPC message request
            context: The gRPC context

        """
        self.validate_collaborator(request, context)
        self.check_request(request)
        collaborator_name = request.header.sender
        dec_request = decrypt_AES(self.cyphers[collaborator_name], request.payload)

        tensor_name = dec_request.tensor_name
        require_lossless = dec_request.require_lossless
        round_number = dec_request.round_number
        report = dec_request.report
        tags = dec_request.tags

        named_tensor = self.aggregator.get_aggregated_tensor(
            collaborator_name, tensor_name, round_number, report, tags, require_lossless)

        '''transformer_metadata = encrypt_AES(self.cyphers[collaborator_name], named_tensor.transformer_metadata)
        for i in named_tensor.transformer_metadata:
            named_tensor.transformer_metadata.remove(i)
        named_tensor = encrypt_AES(self.cyphers[collaborator_name], named_tensor)
        name, round_number, lossless, report, tags, transformer_metadata, data_bytes = encrypt_payload(named_tensor)
        payload = encrypt_AES(self.cyphers[collaborator_name], Payload())'''
        payload = encrypt_named_tensor(named_tensor, self.cyphers[collaborator_name])
        return TensorResponseQKD(header=self.get_header(collaborator_name),
                                 payload=payload)

    def SendLocalTaskResults(self, request, context):  # NOQA:N802
        """
        Request a model download from aggregator.

        Args:
            request: The gRPC message request
            context: The gRPC context

        """
        proto = TaskResults()
        proto = utils.datastream_to_proto(proto, request)

        self.validate_collaborator(proto, context)
        # all messages get sanity checked
        self.check_request(proto)

        collaborator_name = proto.header.sender
        task_name = proto.task_name
        round_number = proto.round_number
        data_size = proto.data_size
        named_tensors = proto.tensors

        self.aggregator.send_local_task_results(
            collaborator_name, round_number, task_name, data_size, named_tensors)
        # turn data stream into local model update
        return Acknowledgement(header=self.get_header(collaborator_name))

    def SendLocalTaskResultsQKD(self, request, context):  # NOQA:N802
        """
        Request a model download from aggregator.

        Args:
            request: The gRPC message request
            context: The gRPC context

        """
        proto = TaskResultsQKD()
        proto = utils.datastream_to_proto(proto, request)

        self.validate_collaborator(proto, context)
        # all messages get sanity checked
        self.check_request(proto)
        collaborator_name = proto.header.sender

        dec_request = decrypt_AES(self.cyphers[collaborator_name], proto.payload)

        task_name = dec_request.task_name
        round_number = dec_request.round_number
        data_size = dec_request.data_size
        named_tensors = dec_request.tensors
        dec_named_tensors = []
        for n in named_tensors:
            dec_named_tensors.append(decrypt_named_tensor(n, self.cyphers[collaborator_name]))
        self.aggregator.send_local_task_results(
            collaborator_name, round_number, task_name, data_size, dec_named_tensors)
        # turn data stream into local model update
        return Acknowledgement(header=self.get_header(collaborator_name))

    def get_server(self):
        """Return gRPC server."""
        self.server = server(ThreadPoolExecutor(max_workers=cpu_count()),
                             options=self.channel_options)

        add_AggregatorServicer_to_server(self, self.server)

        if not self.tls:
            port = self.server.add_insecure_port(self.uri)
            self.logger.info(f'Insecure port: {port}')

        else:

            with open(self.private_key, 'rb') as f:
                private_key_b = f.read()
            with open(self.certificate, 'rb') as f:
                certificate_b = f.read()
            with open(self.root_certificate, 'rb') as f:
                root_certificate_b = f.read()

            if self.disable_client_auth:
                self.logger.warn('Client-side authentication is disabled.')

            self.server_credentials = ssl_server_credentials(
                ((private_key_b, certificate_b),),
                root_certificates=root_certificate_b,
                require_client_auth=not self.disable_client_auth
            )

            self.server.add_secure_port(self.uri, self.server_credentials)

        return self.server

    def serve(self):
        """Start an aggregator gRPC service."""
        self.get_server()

        self.logger.info('Starting Aggregator gRPC Server')
        self.server.start()

        try:
            while not self.aggregator.all_quit_jobs_sent():
                sleep(5)
        except KeyboardInterrupt:
            pass

        self.server.stop(0)

    def get_key(self):
        conn = http.client.HTTPConnection("127.0.0.1:5001")
        conn.request("GET", "/test")
        r = conn.getresponse()
        string = r.read().decode()
        self.logger.info(string)
        keys = json.loads(string)
        key = keys['keys'][0]['key']
        return key
