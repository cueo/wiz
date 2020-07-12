import json
from constants import GET_PILOT


class Params:
    def __init__(self, **kwargs):
        self.params = kwargs

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, value):
        self.params[key] = value

    def __str__(self):
        return json.dumps(self.__dict__)


class Request:
    def __init__(self, method: str, params: Params = None):
        self.method = method
        self.params = None
        if params:
            self.params = params.params

    def __bytes__(self):
        return str(self).encode('utf-8')

    def __str__(self):
        return json.dumps(self.__dict__)


class Config:
    def __init__(self, state=True, scene=11, red=None, green=None, blue=None, brightness=100):
        self.state = state
        self.scene = scene
        self.red = red
        self.green = green
        self.blue = blue
        self.brightness = brightness


if __name__ == '__main__':
    message = Request(GET_PILOT, Params(state=True))
    print(bytes(message).decode('utf-8'))
