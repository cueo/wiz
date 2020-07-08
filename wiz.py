import webcolors

from udp import UDP
from constants import *
from message import Params, Request


class Light:
    def __init__(self, ip: str):
        # TODO: get ip from network auto
        self.ip = ip
        self.udp = UDP(ip)

    def send(self, message):
        self.udp.call(message)

    def on(self):
        params = Params(state=True)
        message = self.message(params)
        self.send(message)

    def off(self):
        params = Params(state=False)
        message = self.message(params)
        # print(message)
        self.send(message)

    def color(self, **kwargs):
        params = Params()
        if HEXCODE in kwargs:
            params['r'] = int(kwargs[HEXCODE][:2], 16)
            params['g'] = int(kwargs[HEXCODE][2:4], 16)
            params['b'] = int(kwargs[HEXCODE][4:], 16)
        elif COLOR in kwargs:
            params['r'], params['g'], params['b'] = webcolors.name_to_rgb(kwargs[COLOR])
        else:
            if RED in kwargs:
                params['r'] = kwargs[RED]
            if BLUE in kwargs:
                params['b'] = kwargs[BLUE]
            if GREEN in kwargs:
                params['g'] = kwargs[GREEN]
        message = self.message(params)
        print(params, message)
        self.send(message)

    def dim(self, value: int):
        params = Params(dimming=value)
        message = self.message(params)
        self.send(message)

    def temp(self, value: int):
        params = Params(temp=value)
        message = self.message(params)
        self.send(message)

    def speed(self, value: int):
        params = Params(speed=value)
        message = self.message(params)
        self.send(message)

    def get_config(self):
        message = Request(GET_PILOT)
        return self.udp.call(message)

    @staticmethod
    def message(params: Params):
        return Request(SET_PILOT, params)


if __name__ == '__main__':
    light = Light(IP)
    light.color(red=255)
