#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.backend import set_session

from arch.api.utils.log_utils import LoggerFactory
from federatedml.framework.weights import OrderDictWeights, Weights
from federatedml.nn.homo_nn.nn_model import NNModel, DataConverter
import copy

Logger = LoggerFactory.get_logger()


def _compile_model(model, loss, optimizer, metrics):
    optimizer_instance = getattr(tf.keras.optimizers, optimizer.optimizer)(**optimizer.kwargs)
    losses = getattr(tf.keras.losses, loss)
    model.compile(loss=losses,
                  optimizer=optimizer_instance,
                  metrics=metrics)
    return model


def _init_session():
    sess = tf.Session()
    tf.get_default_graph()
    set_session(sess)
    return sess


def _load_model(nn_struct_json):
    return tf.keras.models.model_from_json(nn_struct_json, custom_objects={})


def build_keras(nn_define, loss, optimizer, metrics):
    import json
    nn_define_json = json.dumps(nn_define)

    sess = _init_session()
    model = _load_model(nn_struct_json=nn_define_json)
    model = _compile_model(model=model,
                           loss=loss,
                           optimizer=optimizer,
                           metrics=metrics)
    return KerasNNModel(sess, model), KerasSequenceDataConverter()


def from_keras_sequential_model(model, loss, optimizer, metrics):
    sess = _init_session()
    model = _compile_model(model=model,
                           loss=loss,
                           optimizer=optimizer,
                           metrics=metrics)
    return KerasNNModel(sess, model)


class KerasNNModel(NNModel):
    def __init__(self, sess, model):
        self._sess: tf.Session = sess
        self._model: tf.keras.Sequential = model
        self._trainable_weights = {self._trim_device_str(v.name): v for v in self._model.trainable_weights}

    @staticmethod
    def _trim_device_str(name):
        return name.split("/")[0]

    def get_model_weights(self) -> OrderDictWeights:
        return OrderDictWeights(self._sess.run(self._trainable_weights))

    def set_model_weights(self, weights: Weights):
        unboxed = weights.unboxed
        self._sess.run([tf.assign(v, unboxed[name]) for name, v in self._trainable_weights.items()])

    def train(self, data: tf.keras.utils.Sequence, **kwargs):
        epochs = 1
        left_kwargs = copy.deepcopy(kwargs)
        if "aggregate_every_n_epoch" in kwargs:
            epochs = kwargs["aggregate_every_n_epoch"]
            del left_kwargs["aggregate_every_n_epoch"]
        self._model.fit(x=data, epochs=epochs, verbose=1, shuffle=True, **left_kwargs)
        return epochs * len(data)

    def evaluate(self, data: tf.keras.utils.Sequence, **kwargs):
        names = self._model.metrics_names
        values = self._model.evaluate(x=data, verbose=1)
        if not isinstance(values, list):
            values = [values]
        return dict(zip(names, values))

    def predict(self, data: tf.keras.utils.Sequence, **kwargs):
        return self._model.predict(data)


class KerasSequenceData(tf.keras.utils.Sequence):

    def get_shape(self):
        return self.x_shape, self.y_shape

    def __init__(self, data_instances, batch_size):
        self.size = data_instances.count()
        if self.size <= 0:
            raise ValueError("empty data")

        _, one_data = data_instances.first()
        self.x_shape = one_data.features.shape
        self.y_shape = getattr(one_data.label, "shape", (1,))
        self.x = np.zeros((self.size, *self.x_shape))
        self.y = np.zeros((self.size, *self.y_shape))
        index = 0
        self._keys = []
        for k, inst in data_instances.collect():
            self._keys.append(k)
            self.x[index] = inst.features
            self.y[index] = inst.label
            index += 1

        self.batch_size = batch_size if batch_size > 0 else self.size

    def __getitem__(self, index):
        """Gets batch at position `index`.

        # Arguments
            index: position of the batch in the Sequence.

        # Returns
            A batch
        """
        start = self.batch_size * index
        end = self.batch_size * (index + 1)
        return self.x[start: end], self.y[start: end]

    def __len__(self):
        """Number of batch in the Sequence.

        # Returns
            The number of batches in the Sequence.
        """
        return int(np.ceil(self.size / float(self.batch_size)))

    def get_keys(self):
        return self._keys


class KerasSequenceDataConverter(DataConverter):
    def convert(self, data, *args, **kwargs):
        return KerasSequenceData(data, *args, **kwargs)
