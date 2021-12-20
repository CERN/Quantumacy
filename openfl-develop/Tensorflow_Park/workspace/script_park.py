# Install dependencies if not already installed
# !pip install tensorflow==2.3.1

# Create a federation
from openfl.interface.interactive_api.federation import Federation

# please use the same identificator that was used in signed certificate
client_id = 'api'
cert_dir = 'cert'
director_node_fqdn = 'localhost'
# 1) Run with API layer - Director mTLS 
# If the user wants to enable mTLS their must provide CA root chain, and signed key pair to the federation interface
# cert_chain = f'{cert_dir}/root_ca.crt'
# api_certificate = f'{cert_dir}/{client_id}.crt'
# api_private_key = f'{cert_dir}/{client_id}.key'

# federation = Federation(client_id=client_id, director_node_fqdn=director_node_fqdn, director_port='50051',
#                        cert_chain=cert_chain, api_cert=api_certificate, api_private_key=api_private_key)

# --------------------------------------------------------------------------------------------------------------------

# 2) Run with TLS disabled (trusted environment)
# Federation can also determine local fqdn automatically
federation = Federation(client_id=client_id, director_node_fqdn=director_node_fqdn, director_port='50051', tls=False)


shard_registry = federation.get_shard_registry()
print(shard_registry)

# First, request a dummy_shard_desc that holds information about the federated dataset 
dummy_shard_desc = federation.get_dummy_shard_descriptor(size=10)
sample, target = dummy_shard_desc[0]
f"Sample shape: {sample.shape}, target shape: {target.shape}"

from openfl.interface.interactive_api.experiment import TaskInterface, DataInterface, ModelInterface, FLExperiment

from layers import create_model, optimizer, optimized_model
framework_adapter = 'openfl.plugins.frameworks_adapters.keras_adapter.FrameworkAdapterPlugin'
model = create_model()
MI = ModelInterface(model=model, optimizer=optimizer, framework_plugin=framework_adapter)

import numpy as np
from tensorflow.keras.utils import Sequence

class DataGenerator(Sequence):

    def __init__(self, shard_descriptor, batch_size):
        self.shard_descriptor = shard_descriptor
        self.batch_size = batch_size
        self.indices = np.arange(len(shard_descriptor))
        self.on_epoch_end()

    def __len__(self):
        return len(self.indices) // self.batch_size

    def __getitem__(self, index):
        index = self.indices[index * self.batch_size:(index + 1) * self.batch_size]
        batch = [self.indices[k] for k in index]

        X, y = self.shard_descriptor[batch]
        return X, y

    def on_epoch_end(self):
        np.random.shuffle(self.indices)


class ParkFedDataset(DataInterface):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def shard_descriptor(self):
        return self._shard_descriptor

    @shard_descriptor.setter
    def shard_descriptor(self, shard_descriptor):
        """
        Describe per-collaborator procedures or sharding.

        This method will be called during a collaborator initialization.
        Local shard_descriptor will be set by Envoy.
        """
        self._shard_descriptor = shard_descriptor

    def __getitem__(self, index):
        return self.shard_descriptor[index]

    def __len__(self):
        return len(self.shard_descriptor)

    def get_train_loader(self):
        """
        Output of this method will be provided to tasks with optimizer in contract
        """
        if self.kwargs['train_bs']:
            batch_size = self.kwargs['train_bs']
        else:
            batch_size = 32
        self.shard_descriptor.set_dataset_type(mode='train')
        return DataGenerator(self.shard_descriptor, batch_size=batch_size)

    def get_valid_loader(self):
        """
        Output of this method will be provided to tasks without optimizer in contract
        """
        if self.kwargs['valid_bs']:
            batch_size = self.kwargs['valid_bs']
        else:
            batch_size = 32
        
        self.shard_descriptor.set_dataset_type(mode='val')
        return DataGenerator(self.shard_descriptor, batch_size=batch_size)

    def get_train_data_size(self):
        """
        Information for aggregation
        """
        
        return self.shard_descriptor.get_train_size()

    def get_valid_data_size(self):
        """
        Information for aggregation
        """
        return self.shard_descriptor.get_test_size()

fed_dataset = ParkFedDataset(train_bs=64, valid_bs=64)

TI = TaskInterface()

import time
import tensorflow as tf
from layers import train_acc_metric, val_acc_metric, loss_fn

@TI.register_fl_task(model='model', data_loader='train_dataset', \
                     device='device', optimizer='optimizer')     
def train(model, train_dataset, optimizer, device, loss_fn=loss_fn, warmup=False):
    start_time = time.time()
    # Iterate over the batches of the dataset.
    for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):
        with tf.GradientTape() as tape:
            logits = model(x_batch_train, training=True)
            loss_value = loss_fn(y_batch_train, logits)
        grads = tape.gradient(loss_value, model.trainable_weights)
        optimizer.apply_gradients(zip(grads, model.trainable_weights))

        # Update training metric.
        train_acc_metric.update_state(y_batch_train, logits)

        # Log every 200 batches.
        if step % 200 == 0:
            print(
                "Training loss (for one batch) at step %d: %.4f"
                % (step, float(loss_value))
            )
            print("Seen so far: %d samples" % ((step + 1) * 64))
        if warmup:
            break

    # Display metrics at the end of each epoch.
    train_acc = train_acc_metric.result()
    print("Training acc over epoch: %.4f" % (float(train_acc),))

    # Reset training metrics at the end of each epoch
    train_acc_metric.reset_states()

        
    return {'train_acc': train_acc,}


@TI.register_fl_task(model='model', data_loader='val_dataset', device='device')     
def validate(model, val_dataset, device):
    # Run a validation loop at the end of each epoch.
    for x_batch_val, y_batch_val in val_dataset:
        val_logits = model(x_batch_val, training=False)
        # Update val metrics
        val_acc_metric.update_state(y_batch_val, val_logits)
    val_acc = val_acc_metric.result()
    val_acc_metric.reset_states()
    print("Validation acc: %.4f" % (float(val_acc),))
            
    return {'validation_accuracy': val_acc,}

# create an experiment in federation
experiment_name = 'Parkinson_experiment'
fl_experiment = FLExperiment(federation=federation, experiment_name=experiment_name)

# The following command zips the workspace and python requirements to be transfered to collaborator nodes
fl_experiment.start(model_provider=MI, 
                   task_keeper=TI,
                   data_loader=fed_dataset,
                   rounds_to_train=5,
                   opt_treatment='CONTINUE_GLOBAL')

fl_experiment.stream_metrics()
