import numpy as np
from collections.abc import MutableMapping


class BasicTerrain:
    def __init__(self, params, lower_layer_mask):
        self._needed_params = []
        self._params = self.ParamsDict({})
        self.params = params
        self._lower_layer_mask = None
        self.lower_layer_mask = lower_layer_mask

    def __str__(self):
        return str(self.params)

    class ParamsDict(MutableMapping, dict):
        def __getitem__(self, key):
            return dict.__getitem__(self, key)

        def __setitem__(self, key, value):
            key = str(key)
            if key not in BasicTerrain.get_available_params():
                raise ValueError(f'{key} is not in available keys')

            if key == 'count':
                if type(value) != int:
                    raise TypeError("count is not an integer")
                if value < 0:
                    raise ValueError("count has wrong value")

            elif key == 'color':
                if type(value) != str:
                    raise TypeError("color is not a string")

            elif key == 'percentage':
                if type(value) != float:
                    raise TypeError("percentage is not a float")
                if value < 0. or value > 1.:
                    raise ValueError("percentage has wrong value")

            dict.__setitem__(self, key, value)

        def __delitem__(self, key):
            dict.__delitem__(self, key)

        def __iter__(self):
            return dict.__iter__(self)

        def __len__(self):
            return dict.__len__(self)

        def __contains__(self, x):
            return dict.__contains__(self, x)

    @staticmethod
    def get_available_params():
        return [
            'count',
            'color',
            'percentage',
        ]

    @staticmethod
    def verify_layer(layer, desired_type, layer_name="layer"):
        if type(layer) != np.ndarray:
            raise TypeError(f"{layer_name} is not numpy ndarray type")
        if layer.ndim != 2:
            raise TypeError(f"{layer_name} is not 2d array")
        if layer.dtype != desired_type:
            raise TypeError(f"{layer_name} dtype is not a boolean")

    def generate_layer(self, seed):
        layer_mask = self.lower_layer_mask
        return layer_mask

    @property
    def needed_params(self):
        return self._needed_params

    @property
    def lower_layer_mask(self):
        return self._lower_layer_mask

    @lower_layer_mask.setter
    def lower_layer_mask(self, lower_layer_mask):
        self.verify_layer(lower_layer_mask, bool, "lower_layer_mask")
        self._lower_layer_mask = lower_layer_mask

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        for param in self.needed_params:
            if param not in params:
                raise ValueError("parameters given to params setter are not valid")

        if type(params) != dict:
            raise TypeError("basic terrain is not dict")
        try:
            tmp_params_dict = self.ParamsDict()
            for key in params:
                tmp_params_dict[key] = params[key]
        except TypeError as err:
            raise ValueError("parameters values given to params setter are not valid:" + " TypeError: " + str(err))
        except ValueError as err:
            raise ValueError("parameters values given to params setter are not valid:" + " ValueError: " + str(err))
        self._params = tmp_params_dict


class Island(BasicTerrain):
    def __init__(self, params, lower_layer):
        super().__init__(params, lower_layer)
        self._needed_params = [
            'count',
            'color',
            'percentage',
        ]


lower_layer = np.ones((30, 15), dtype=bool)
params = {
    'count':1,
    'color':'green',
    'percentage': 0.4,
}
a = Island(params, lower_layer)
print(a)