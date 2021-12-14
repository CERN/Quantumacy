#!/usr/bin/env python
# coding: utf-8

# # Federated Market with Director example
# ## Using low-level Python API

# # Long-Living entities update
# 
# * We now may have director running on another machine.
# * We use Federation API to communicate with Director.
# * Federation object should hold a Director's client (for user service)
# * Keeping in mind that several API instances may be connacted to one Director.
# 
# 
# * We do not think for now how we start a Director.
# * But it knows the data shape and target shape for the DataScience problem in the Federation.
# * Director holds the list of connected envoys, we do not need to specify it anymore.
# * Director and Envoys are responsible for encrypting connections, we do not need to worry about certs.
# 
# 
# * Yet we MUST have a cert to communicate to the Director.
# * We MUST know the FQDN of a Director.
# * Director communicates data and target shape to the Federation interface object.
# 
# 
# * Experiment API may use this info to construct a dummy dataset and a `shard descriptor` stub.

# In[ ]:


# Install dependencies if not already installed
# !pip install -r requirements.txt


# # Connect to the Federation

# In[4]:


# Create a federation
from openfl.interface.interactive_api.federation import Federation

# please use the same identificator that was used in signed certificate
cliend_id = 'frontend'

# 1) Run with API layer - Director mTLS 
# If the user wants to enable mTLS their must provide CA root chain, and signed key pair to the federation interface
# cert_chain = 'cert/root_ca.crt'
# API_certificate = 'cert/frontend.crt'
# API_private_key = 'cert/frontend.key'

# federation = Federation(client_id='frontend', director_node_fqdn='localhost', director_port='50051', disable_tls=False,
#                        cert_chain=cert_chain, api_cert=API_certificate, api_private_key=API_private_key)

# --------------------------------------------------------------------------------------------------------------------

# 2) Run with TLS disabled (trusted environment)
# Federation can also determine local fqdn automatically
federation = Federation(client_id='frontend', director_node_fqdn='localhost', director_port='50051', tls=False)


# In[ ]:


shard_registry = federation.get_shard_registry()
shard_registry


# In[ ]:


federation.target_shape


# In[7]:


# First, request a dummy_shard_desc that holds information about the federated dataset 
dummy_shard_desc = federation.get_dummy_shard_descriptor(size=10)
sample, target = dummy_shard_desc[0]


# ## Creating a FL experiment using Interactive API

# In[8]:


from openfl.interface.interactive_api.experiment import TaskInterface, DataInterface, ModelInterface, FLExperiment


# ### Register dataset

# We extract User dataset class implementation.
# Is it convinient?
# What if the dataset is not a class?

# In[9]:


from copy import deepcopy

from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import Compose, Normalize, RandomHorizontalFlip, Resize, ToTensor

from tools import RandomIdentitySampler
import transforms as T


# Now you can implement you data loaders using dummy_shard_desc
class ImageDataset(Dataset):
    """Image Person ReID Dataset."""

    def __init__(self, dataset, transform=None):
        """Initialize Dataset."""
        self.dataset = dataset
        self.transform = transform

    def __len__(self):
        """Length of dataset."""
        return len(self.dataset)

    def __getitem__(self, index):
        """Get item from dataset."""
        img, (pid, camid) = self.dataset[index]
        if self.transform is not None:
            img = self.transform(img)
        return img, (pid, camid)


class MarketFLDataloader(DataInterface):
    """Market Dataset."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Prepare transforms
        self.transform_train = Compose([
            T.ResizeRandomCropping(256, 128, p=0.5),
            RandomHorizontalFlip(),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            T.RandomErasing(probability=0.5)
        ])
        self.transform_test = Compose([
            Resize((265, 128)),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

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

    def get_train_loader(self, **kwargs):
        """
        Output of this method will be provided to tasks with optimizer in contract.
        """
        if self.kwargs['train_bs']:
            batch_size = self.kwargs['train_bs']
        else:
            batch_size = 64

        self.shard_descriptor.set_mode('train')
        return DataLoader(
            # ImageDataset make transform
            ImageDataset(self.shard_descriptor, transform=self.transform_train),
            sampler=RandomIdentitySampler(self.shard_descriptor, num_instances=4),
            batch_size=batch_size, num_workers=4, pin_memory=True, drop_last=True
        )

    def get_valid_loader(self, **kwargs):
        """
        Output of this method will be provided to tasks without optimizer in contract.
        """
        if self.kwargs['valid_bs']:
            batch_size = self.kwargs['valid_bs']
        else:
            batch_size = 512

        query_sd_copy = deepcopy(self.shard_descriptor)
        query_sd_copy.set_mode('query')
        query_loader = DataLoader(ImageDataset(query_sd_copy, transform=self.transform_test),
                       batch_size=batch_size, num_workers=4, pin_memory=True,
                       drop_last=False, shuffle=False)

        gallery_sd_copy = deepcopy(self.shard_descriptor)
        gallery_sd_copy.set_mode('gallery')
        gallery_loader = DataLoader(ImageDataset(gallery_sd_copy, transform=self.transform_test),
                       batch_size=batch_size, num_workers=4, pin_memory=True,
                       drop_last=False, shuffle=False)

        return query_loader, gallery_loader

    def get_train_data_size(self):
        """
        Information for aggregation.
        """
        return len(self.shard_descriptor.train_path)

    def get_valid_data_size(self):
        """
        Information for aggregation.
        """
        return len(self.shard_descriptor.gal_path)


# In[10]:


fed_dataset = MarketFLDataloader(train_bs=64, valid_bs=512)


# ### Describe a model and optimizer

# In[11]:


import torch
import torch.nn as nn
import torch.optim as optim
import torchvision


# In[12]:


"""
ResNet and Classifier definition
"""

class ResNet50(nn.Module):
    "Pretrained ResNet50."

    def __init__(self, **kwargs):
        super().__init__()
        
        self.classifier = NormalizedClassifier()

        resnet50 = torchvision.models.resnet50(pretrained=True)
        resnet50.layer4[0].conv2.stride = (1, 1)
        resnet50.layer4[0].downsample[0].stride = (1, 1)
        self.base = nn.Sequential(*list(resnet50.children())[:-2])

        self.bn = nn.BatchNorm1d(2048)
        nn.init.normal_(self.bn.weight.data, 1.0, 0.02)
        nn.init.constant_(self.bn.bias.data, 0.0)

    def forward(self, x):
        x = self.base(x)
        x = nn.functional.avg_pool2d(x, x.size()[2:])
        x = x.view(x.size(0), -1)
        f = self.bn(x)

        return f


class NormalizedClassifier(nn.Module):
    """Classifier."""

    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.Tensor(1501, 2048))
        self.weight.data.uniform_(-1, 1).renorm_(2,0,1e-5).mul_(1e5)

    def forward(self, x):
        w = self.weight

        x = nn.functional.normalize(x, p=2, dim=1)
        w = nn.functional.normalize(w, p=2, dim=1)

        return nn.functional.linear(x, w)


resnet = ResNet50()


# In[ ]:


parameters = list(resnet.parameters()) + list(resnet.classifier.parameters())
optimizer_adam = optim.Adam(parameters, lr=1e-4)


# #### Register model

# In[14]:


framework_adapter = 'openfl.plugins.frameworks_adapters.pytorch_adapter.FrameworkAdapterPlugin'
MI = ModelInterface(model=resnet, optimizer=optimizer_adam, framework_plugin=framework_adapter)
# Save the initial model state
initial_model = deepcopy(resnet)


# ### Define and register FL tasks

# In[15]:


TI = TaskInterface()

from logging import getLogger

import torch
import tqdm

from losses import ArcFaceLoss, TripletLoss
from tools import AverageMeter, evaluate, extract_feature

logger = getLogger(__name__)

# Task interface currently supports only standalone functions.
@TI.register_fl_task(model='model', data_loader='train_loader',
                     device='device', optimizer='optimizer')
def train(model, train_loader, optimizer, device):
    device = torch.device('cuda')
    
    criterion_cla = ArcFaceLoss(scale=16., margin=0.1)
    criterion_pair = TripletLoss(margin=0.3, distance='cosine')

    batch_cla_loss = AverageMeter()
    batch_pair_loss = AverageMeter()
    corrects = AverageMeter()
    
    model.train()
    model.to(device)
    model.classifier.train()
    model.classifier.to(device)
    
    logger.info('==> Start training')
    train_loader = tqdm.tqdm(train_loader, desc='train')

    for imgs, (pids, _) in train_loader:
        imgs, pids = torch.tensor(imgs).to(device), torch.tensor(pids).to(device)
        # Zero the parameter gradients
        optimizer.zero_grad()
        # Forward
        features = model(imgs)
        outputs = model.classifier(features)
        _, preds = torch.max(outputs.data, 1)
        # Compute loss
        cla_loss = criterion_cla(outputs, pids)
        pair_loss = criterion_pair(features, pids)
        loss = cla_loss + pair_loss
        # Backward + Optimize
        loss.backward()
        optimizer.step()
        # statistics
        corrects.update(torch.sum(preds == pids.data).float() / pids.size(0), pids.size(0))
        batch_cla_loss.update(cla_loss.item(), pids.size(0))
        batch_pair_loss.update(pair_loss.item(), pids.size(0))

    return {'ArcFaceLoss': batch_cla_loss.avg,
            'TripletLoss': batch_pair_loss.avg,
            'Accuracy': corrects.avg.cpu()}


@TI.register_fl_task(model='model', data_loader='val_loader', device='device')
def validate(model, val_loader, device):
    queryloader, galleryloader = val_loader
    device = torch.device('cuda')
    
    logger.info('==> Start validating')
    model.eval()
    model.to(device)
    
    # Extract features for query set
    qf, q_pids, q_camids = extract_feature(model, queryloader)
    logger.info(f'Extracted features for query set, obtained {qf.shape} matrix')
    # Extract features for gallery set
    gf, g_pids, g_camids = extract_feature(model, galleryloader)
    logger.info(f'Extracted features for gallery set, obtained {gf.shape} matrix')
    # Compute distance matrix between query and gallery
    m, n = qf.size(0), gf.size(0)
    distmat = torch.zeros((m,n))
    # Cosine similarity
    qf = nn.functional.normalize(qf, p=2, dim=1)
    gf = nn.functional.normalize(gf, p=2, dim=1)
    for i in range(m):
        distmat[i] = - torch.mm(qf[i:i+1], gf.t())
    distmat = distmat.numpy()

    cmc, mAP = evaluate(distmat, q_pids, g_pids, q_camids, g_camids)
    return {'top1': cmc[0], 'top5': cmc[4], 'top10': cmc[9], 'mAP': mAP}


# ## Time to start a federated learning experiment

# In[16]:


# create an experimnet in federation
experiment_name = 'market_test_experiment'
fl_experiment = FLExperiment(federation=federation, experiment_name=experiment_name)


# In[ ]:


# If I use autoreload I got a pickling error

# The following command zips the workspace and python requirements to be transfered to collaborator nodes
fl_experiment.start(model_provider=MI, 
                    task_keeper=TI,
                    data_loader=fed_dataset,
                    rounds_to_train=3,
                    opt_treatment='RESET')


# In[ ]:


# If user want to stop IPython session, then reconnect and check how experiment is going 
# fl_experiment.restore_experiment_state(MI)

fl_experiment.stream_metrics(tensorboard_logs=False)

