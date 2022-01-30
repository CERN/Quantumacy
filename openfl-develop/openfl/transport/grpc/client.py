# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""CollaboratorGRPCClient module."""
import logging
import time
from logging import getLogger
from typing import Optional
from typing import Tuple

import grpc
import http.client
import json

from cryptography.fernet import Fernet

from openfl.protocols import Acknowledgement
from openfl.protocols import AggregatorStub
from openfl.protocols import MessageHeader
from openfl.protocols import TaskResults
from openfl.protocols import TaskResultsQKD
from openfl.protocols import TasksRequest
from openfl.protocols import TensorRequest
from openfl.protocols import TensorRequestQKD
from openfl.protocols import NamedTensor
from openfl.protocols import MetadataProto
from openfl.protocols import utils
from openfl.utilities import check_equal
from openfl.protocols.utils import encrypt_AES, encrypt_named_tensor, decrypt_named_tensor
from openfl.protocols.utils import decrypt_AES


class ConstantBackoff:
    """Constant Backoff policy."""

    def __init__(self, reconnect_interval, logger, uri):
        """Initialize Constant Backoff."""
        self.reconnect_interval = reconnect_interval
        self.logger = logger
        self.uri = uri

    def sleep(self):
        """Sleep for specified interval."""
        self.logger.info(f'Attempting to connect to aggregator at {self.uri}')
        time.sleep(self.reconnect_interval)


class RetryOnRpcErrorClientInterceptor(
    grpc.UnaryUnaryClientInterceptor, grpc.StreamUnaryClientInterceptor
):
    """Retry gRPC connection on failure."""

    def __init__(
            self,
            sleeping_policy,
            status_for_retry: Optional[Tuple[grpc.StatusCode]] = None,
    ):
        """Initialize function for gRPC retry."""
        self.sleeping_policy = sleeping_policy
        self.status_for_retry = status_for_retry

    def _intercept_call(self, continuation, client_call_details, request_or_iterator):
        """Intercept the call to the gRPC server."""
        while True:
            response = continuation(client_call_details, request_or_iterator)

            if isinstance(response, grpc.RpcError):
                return response
                # If status code is not in retryable status codes
                self.sleeping_policy.logger.info(f'Response code: {response.code()}')
                if (
                        self.status_for_retry
                        and response.code() not in self.status_for_retry
                ):
                    return response

                self.sleeping_policy.sleep()
            else:
                return response

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Wrap intercept call for unary->unary RPC."""
        return self._intercept_call(continuation, client_call_details, request)

    def intercept_stream_unary(
            self, continuation, client_call_details, request_iterator
    ):
        """Wrap intercept call for stream->unary RPC."""
        return self._intercept_call(continuation, client_call_details, request_iterator)


def _atomic_connection(func):
    def wrapper(self, *args, **kwargs):
        self.reconnect()
        response = func(self, *args, **kwargs)
        self.disconnect()
        return response

    return wrapper


class CollaboratorGRPCClient:
    """Collaboration over gRPC-TLS."""

    def __init__(self,
                 agg_addr,
                 agg_port,
                 tls,
                 disable_client_auth,
                 root_certificate,
                 certificate,
                 private_key,
                 aggregator_uuid=None,
                 federation_uuid=None,
                 single_col_cert_common_name=None,
                 **kwargs):
        """Initialize."""
        self.uri = f'{agg_addr}:{agg_port}'
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

        self.logger = getLogger(__name__)

        if not self.tls:
            self.channel = self.create_insecure_channel(self.uri)
        else:
            self.channel = self.create_tls_channel(
                self.uri,
                self.root_certificate,
                self.disable_client_auth,
                self.certificate,
                self.private_key
            )

        self.header = None
        self.aggregator_uuid = aggregator_uuid
        self.federation_uuid = federation_uuid
        self.single_col_cert_common_name = single_col_cert_common_name

        # Adding an interceptor for RPC Errors
        self.interceptors = (
            RetryOnRpcErrorClientInterceptor(
                sleeping_policy=ConstantBackoff(
                    logger=self.logger,
                    reconnect_interval=int(kwargs.get('client_reconnect_interval', 1)),
                    uri=self.uri),
                status_for_retry=(grpc.StatusCode.UNAVAILABLE,),
            ),
        )
        self.stub = AggregatorStub(
            grpc.intercept_channel(self.channel, *self.interceptors)
        )

        # qkd
        self.qkd = True
        self.cypher = None

    def create_insecure_channel(self, uri):
        """
        Set an insecure gRPC channel (i.e. no TLS) if desired.

        Warns user that this is not recommended.

        Args:
            uri: The uniform resource identifier fo the insecure channel

        Returns:
            An insecure gRPC channel object

        """
        return grpc.insecure_channel(uri, options=self.channel_options)

    def create_tls_channel(self, uri, root_certificate, disable_client_auth,
                           certificate, private_key):
        """
        Set an secure gRPC channel (i.e. TLS).

        Args:
            uri: The uniform resource identifier fo the insecure channel
            root_certificate: The Certificate Authority filename
            disable_client_auth (boolean): True disabled client-side
             authentication (not recommended, throws warning to user)
            certificate: The client certficate filename from the collaborator
             (signed by the certificate authority)

        Returns:
            An insecure gRPC channel object
        """
        with open(root_certificate, 'rb') as f:
            root_certificate_b = f.read()

        if disable_client_auth:
            self.logger.warn('Client-side authentication is disabled.')
            private_key_b = None
            certificate_b = None
        else:
            with open(private_key, 'rb') as f:
                private_key_b = f.read()
            with open(certificate, 'rb') as f:
                certificate_b = f.read()

        credentials = grpc.ssl_channel_credentials(
            root_certificates=root_certificate_b,
            private_key=private_key_b,
            certificate_chain=certificate_b,
        )

        return grpc.secure_channel(
            uri, credentials, options=self.channel_options)

    def _set_header(self, collaborator_name):
        self.header = MessageHeader(
            sender=collaborator_name,
            receiver=self.aggregator_uuid,
            federation_uuid=self.federation_uuid,
            single_col_cert_common_name=self.single_col_cert_common_name or ''
        )

    def validate_response(self, reply, collaborator_name):
        """Validate the aggregator response."""
        # check that the message was intended to go to this collaborator
        check_equal(reply.header.receiver, collaborator_name, self.logger)
        check_equal(reply.header.sender, self.aggregator_uuid, self.logger)

        # check that federation id matches
        check_equal(
            reply.header.federation_uuid,
            self.federation_uuid,
            self.logger
        )

        # check that there is aggrement on the single_col_cert_common_name
        check_equal(
            reply.header.single_col_cert_common_name,
            self.single_col_cert_common_name or '',
            self.logger
        )

    def disconnect(self):
        """Close the gRPC channel."""
        self.logger.debug(f'Disconnecting from gRPC server at {self.uri}')
        self.channel.close()

    def reconnect(self):
        """Create a new channel with the gRPC server."""
        # channel.close() is idempotent. Call again here in case it wasn't issued previously
        self.disconnect()

        if not self.tls:
            self.channel = self.create_insecure_channel(self.uri)
        else:
            self.channel = self.create_tls_channel(
                self.uri,
                self.root_certificate,
                self.disable_client_auth,
                self.certificate,
                self.private_key
            )

        self.logger.debug(f'Connecting to gRPC at {self.uri}')

        self.stub = AggregatorStub(
            grpc.intercept_channel(self.channel, *self.interceptors)
        )

    def get_key(self, id):
        conn = http.client.HTTPConnection("127.0.0.1:5003")
        conn.request("GET", "/test?ID=" + id)
        r = conn.getresponse()
        string = r.read().decode()
        logging.info(string)
        keys = json.loads(string)
        key = keys['keys'][0]['key']
        return key

    def signal_key(self, collaborator_name):
        self._set_header(collaborator_name)
        request = Acknowledgement(header=self.header)
        logging.info("asking key")
        response = self.stub.GetKey.future(request)
        logging.info("getting key")
        self.cypher = Fernet(self.get_key(collaborator_name).encode())
        response = response.result()
        self.validate_response(response, collaborator_name)

    @_atomic_connection
    def get_tasks(self, collaborator_name):
        """Get tasks from the aggregator."""
        self._set_header(collaborator_name)
        request = TasksRequest(header=self.header)
        if self.qkd:
            if self.cypher is None:
                self.signal_key(collaborator_name)
            response = self.stub.GetTasksQKD(request)
            self.validate_response(response, collaborator_name)
            payload = decrypt_AES(self.cypher, response.payload)
            return payload.tasks, payload.round_number, payload.sleep_time, payload.quit
        else:
            response = self.stub.GetTasks(request)
            self.validate_response(response, collaborator_name)
            return response.tasks, response.round_number, response.sleep_time, response.quit

    @_atomic_connection
    def get_aggregated_tensor(self, collaborator_name, tensor_name, round_number,
                              report, tags, require_lossless):
        """Get aggregated tensor from the aggregator."""
        self._set_header(collaborator_name)
        if self.qkd:
            class Payload:
                def __init__(self):
                    self.tensor_name = tensor_name
                    self.round_number = round_number
                    self.report = report
                    self.tags = tags
                    self.require_lossless = require_lossless

            payload_request = encrypt_AES(self.cypher, Payload())
            request = TensorRequestQKD(
                header=self.header,
                payload=payload_request
            )
            response = self.stub.GetAggregatedTensorQKD(request)
            '''payload_response = decrypt_AES(self.cypher, response.payload)
            #named_tensor = decrypt_AES(self.cypher, payload_response.named_tensor)
            payload_response.named_tensor.name = decrypt_AES(self.cypher, payload_response.name)
            payload_response.named_tensor.transformer_metadata = decrypt_AES(self.cypher, payload_response.transformer_metadata)'''
            named_tensor = decrypt_named_tensor(response.payload, self.cypher)
            self.validate_response(response, collaborator_name)
            return named_tensor
        else:
            request = TensorRequest(
                header=self.header,
                tensor_name=tensor_name,
                round_number=round_number,
                report=report,
                tags=tags,
                require_lossless=require_lossless
            )
            response = self.stub.GetAggregatedTensor(request)
            # also do other validation, like on the round_number
            self.validate_response(response, collaborator_name)
            return response.tensor

    @_atomic_connection
    def send_local_task_results(self, collaborator_name, round_number,
                                task_name, data_size, named_tensors):
        """Send task results to the aggregator."""
        self._set_header(collaborator_name)
        if self.qkd:
            enc_named_tensor = []
            for n in named_tensors:
                enc_named_tensor.append(encrypt_named_tensor(n, self.cypher))
            class Payload:
                def __init__(self):
                    self.round_number = round_number
                    self.task_name = task_name
                    self.data_size = data_size
                    self.tensors = enc_named_tensor

            request = TaskResultsQKD(
                header=self.header,
                payload=encrypt_AES(self.cypher, Payload()))

            stream = []
            stream += utils.proto_to_datastream(request, self.logger)
            response = self.stub.SendLocalTaskResultsQKD(iter(stream))

            self.validate_response(response, collaborator_name)

        else:
            request = TaskResults(
                header=self.header,
                round_number=round_number,
                task_name=task_name,
                data_size=data_size,
                tensors=named_tensors
            )

            # convert (potentially) long list of tensors into stream
            stream = []
            stream += utils.proto_to_datastream(request, self.logger)
            response = self.stub.SendLocalTaskResults(iter(stream))

            # also do other validation, like on the round_number
            self.validate_response(response, collaborator_name)