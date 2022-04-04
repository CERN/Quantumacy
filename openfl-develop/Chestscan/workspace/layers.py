# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Useful keras functions."""

from tensorflow import keras
from tensorflow.keras import layers

def create_model():
    # 2. Model Construction
    model = keras.Sequential()
    model.add(layers.Flatten(input_shape=(128,128,1)))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model
    model = keras.Sequential()
    model.add(layers.Flatten(input_shape=(128,128,1)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.build((128, 128, 1))
    return model


# Instantiate an optimizer.
# Instantiate a loss function.


optimizer = keras.optimizers.SGD(learning_rate=0.008, momentum=0.9)


def loss(labels, logits):
    return keras.losses.binary_crossentropy(labels, logits, from_logits=True)


# Prepare the metrics.
train_acc_metric = keras.metrics.Accuracy()
val_acc_metric = keras.metrics.Accuracy()
