import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
import openfl.native as fx
from openfl.federated import FederatedModel, FederatedDataSet
import random
import warnings
import matplotlib.pyplot as plt
from openfl.utilities.optimizers.torch import FedProxOptimizer

warnings.filterwarnings('ignore')


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)


set_seed(10)

# Setup default workspace, logging, etc.
fx.init('torch_cnn_mnist')


def one_hot(labels, classes):
    return np.eye(classes)[labels]


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.MNIST(root='./data', train=True,
                                      download=True, transform=transform)

train_images, train_labels = trainset.train_data, np.array(trainset.train_labels)
train_images = torch.from_numpy(np.expand_dims(train_images, axis=1)).float()
train_labels = one_hot(train_labels, 10)

validset = torchvision.datasets.MNIST(root='./data', train=False,
                                      download=True, transform=transform)

valid_images, valid_labels = validset.test_data, np.array(validset.test_labels)
valid_images = torch.from_numpy(np.expand_dims(valid_images, axis=1)).float()
valid_labels = one_hot(valid_labels, 10)

feature_shape = train_images.shape[1]
classes = 10

fl_data = FederatedDataSet(train_images, train_labels, valid_images, valid_labels, batch_size=32, num_classes=classes)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3)
        self.fc1 = nn.Linear(32 * 5 * 5, 32)
        self.fc2 = nn.Linear(32, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim=1)

    def train_epoch(self, batch_generator):
        from openfl.federated.task import PyTorchTaskRunner
        self.optimizer.set_old_weights([p for p in self.parameters()])
        return PyTorchTaskRunner.train_epoch(self, batch_generator)


optimizer = lambda x: FedProxOptimizer(x, lr=1e-3, mu=0.1)


def cross_entropy(output, target):
    """Binary cross-entropy metric
    """
    return F.binary_cross_entropy_with_logits(input=output, target=target.float())


# Create a federated model using the pytorch class, lambda optimizer function, and loss function
fl_model = FederatedModel(build_model=Net, optimizer=optimizer, loss_fn=cross_entropy, data_loader=fl_data)
collaborator_models = fl_model.setup(num_collaborators=2)
collaborators = {'one': collaborator_models[0], 'two': collaborator_models[1]}  # , 'three':collaborator_models[2]}

# Original MNIST dataset
print(f'Original training data size: {len(train_images)}')
print(f'Original validation data size: {len(valid_images)}\n')

# Collaborator one's data
print(f'Collaborator one\'s training data size: {len(collaborator_models[0].data_loader.X_train)}')
print(f'Collaborator one\'s validation data size: {len(collaborator_models[0].data_loader.X_valid)}\n')

# Collaborator two's data
print(f'Collaborator two\'s training data size: {len(collaborator_models[1].data_loader.X_train)}')
print(f'Collaborator two\'s validation data size: {len(collaborator_models[1].data_loader.X_valid)}\n')

# Collaborator three's data
# print(f'Collaborator three\'s training data size: {len(collaborator_models[2].data_loader.X_train)}')
# print(f'Collaborator three\'s validation data size: {len(collaborator_models[2].data_loader.X_valid)}')
# Get the current values of the plan. Each of these can be overridden
import json

print(json.dumps(fx.get_plan(), indent=4, sort_keys=True))
# Run experiment, return trained FederatedModel
final_fl_model = fx.run_experiment(collaborators, {'aggregator.settings.rounds_to_train': 1})
# Save final model
final_fl_model.save_native('final_pytorch_model')
