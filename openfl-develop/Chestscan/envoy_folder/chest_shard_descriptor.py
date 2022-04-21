# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Chest Shard Descriptor."""

import logging
import os

import numpy as np
import requests

from openfl.interface.interactive_api.shard_descriptor import ShardDescriptor

logger = logging.getLogger(__name__)


class ChestShardDescriptor(ShardDescriptor):
    """Chest Shard descriptor class."""

    def __init__(
            self,
            rank_worldsize: str = '1, 1',
            **kwargs
    ):
        """Initialize ChestShardDescriptor."""
        self.rank, self.worldsize = tuple(int(num) for num in rank_worldsize.split(','))
        (x_train, y_train), (x_test, y_test) = self.download_data()
        self.x_train = x_train[self.rank - 1::self.worldsize]
        self.y_train = y_train[self.rank - 1::self.worldsize]
        self.x_test = x_test[self.rank - 1::self.worldsize]
        self.y_test = y_test[self.rank - 1::self.worldsize]
        self.dataset_mode = None

    def set_dataset_type(self, mode='train'):
        """Select training or testing mode."""
        self.dataset_mode = mode

    def get_train_size(self):
        """Return train dataset size."""
        return len(self.x_train)

    def get_test_size(self):
        """Return test dataset size."""
        return len(self.x_test)

    def download_data(self):
        def preprocess(x):
            x = x.astype(np.float32) / 255  # gray scale to floating point
            x = np.expand_dims(x, axis=3)
            return x
        # TODO: insert your path
        base_path = ''

        x_train = np.load(base_path + 'train_img.npy')
        x_train = preprocess(x_train)
        y_train = np.load(base_path + 'train_labels.npy')
        y_train = np.asarray(y_train).astype('float32').reshape((-1, 1))

        x_val = np.load(base_path + 'valid_img.npy')
        x_val = preprocess(x_val)

        y_val = np.load(base_path + 'valid_labels.npy')
        y_val = np.asarray(y_val).astype('float32').reshape((-1, 1))

        return (x_train, y_train), (x_val, y_val)

    def __getitem__(self, index: int):
        """Return an item by the index."""
        if self.dataset_mode == 'train':
            return self.x_train[index], self.y_train[index]
        else:
            return self.x_test[index], self.y_test[index]

    @property
    def sample_shape(self):
        """Return the sample shape info."""
        return ['128', '128', '1']

    @property
    def target_shape(self):
        """Return the target shape info."""
        return ['1']

    @property
    def dataset_description(self) -> str:
        """Return the dataset description."""
        return (f'Chest scan dataset, shard number {self.rank}'
                f' out of {self.worldsize}')

    def __len__(self):
        """Return the len of the dataset."""
        if self.dataset_mode is None:
            return 0

        if self.dataset_mode == 'train':
            return len(self.x_train)
        else:
            return len(self.x_test)
