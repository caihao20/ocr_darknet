import os

_config_ = {
    'graph_path': 'data/tensorflow_model/200116_east_model_weights.pb'
}


def get(name):
    return os.path.join(os.path.dirname(__file__), _config_[name]).replace('\\','/')
