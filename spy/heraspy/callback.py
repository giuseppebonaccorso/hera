from keras.callbacks import Callback
import json
import numpy as np

def get_json_type(obj):

    # if obj is any numpy type
    if type(obj).__module__ == np.__name__:
        return obj.item();

    # if obj is a python 'type'
    if type(obj).__name__ == type.__name__:
        return obj.__name__

    raise TypeError('Not JSON Serializable')

def to_json(config):
    return json.dumps(config, default=get_json_type)


class HeraCallback(Callback):
    '''
        A Keras callback
    '''

    def __init__(
            self,
            model_config,
            socket_connection,
            callbacks=[],
            queue_length=10
        ):
        self.model_config = model_config
        self.socket_connection = socket_connection
        super(HeraCallback, self).__init__()

    def on_train_begin(self, logs={}):
        self.socket_connection.emit(
            'train-begin',
            {
                'model': to_json(self.model_config),
                'kerasConfig': to_json(self.model.to_json()),
            }
        )

    def on_batch_end(self, batch, logs={}):
        self.socket_connection.emit(
            'batch-end',
            to_json({
                'model': self.model_config,
                'logs':to_json(logs)
            })
        )

    def on_epoch_end(self, batch, logs={}):
        self.socket_connection.emit(
            'epoch-end',
            to_json({
                'model': self.model_config,
                'logs':to_json(logs)
            })
        )