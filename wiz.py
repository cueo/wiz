import json

import webcolors

from constants import *
from message import Config, Params, Request
from scenes import SCENES
from udp import UDP


class Light:
    def __init__(self, ip: str):
        # TODO: get ip from network auto
        self.ip = ip
        self.udp = UDP(ip)
        self.config = self.get_config()

    def send(self, message):
        result = self.udp.call(message)
        if message.params:
            self.update_config(message.params)
        return result

    def on(self):
        params = Params(state=True)
        message = self.message(params)
        self.send(message)

    def off(self):
        params = Params(state=False)
        message = self.message(params)
        self.send(message)

    def switch(self):
        if self.config.state:
            self.off()
        else:
            self.on()

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
        self.send(message)

    def brightness(self, value: int):
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

    def scene(self, scene_id=None, scene=None):
        if scene:
            if scene in SCENES:
                scene_id = SCENES[scene]
        if not scene_id:
            scene_id = input(self.get_prompt())
        params = Params(sceneId=scene_id)
        message = self.message(params)
        self.send(message)

    def get_config(self):
        message = Request(GET_PILOT)
        result_json = self.send(message).decode('UTF-8')
        result = json.loads(result_json)['result']
        config = Config(state=result['state'], scene=result['sceneId'], brightness=result['dimming'])
        if 'r' in result:
            config.red = result['r']
            config.green = result['g']
            config.blue = result['b']
        return config

    def update_config(self, params):
        for key, value in params.items():
            if key == 'sceneId':
                self.config.scene = params['sceneId']
            if key == 'r':
                self.config.red = params['r']
            elif key == 'g':
                self.config.green = params['g']
            elif key == 'b':
                self.config.blue = params['b']
            elif key == 'dimming':
                self.config.brightness = params['dimming']
            elif key == 'state':
                self.config.state = params['state']

    @staticmethod
    def message(params: Params):
        return Request(SET_PILOT, params)

    @staticmethod
    def get_prompt():
        prompt = 'Select one of the following scenes:\n'
        for scene, scene_id in SCENES.items():
            prompt += '{:>3} : {}\n'.format(scene_id, scene)
        return prompt


if __name__ == '__main__':
    light = Light(IP)
    light.scene()
    light.color(red=255)
    light.switch()
