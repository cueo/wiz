# 💡 wiz
Control Philips Wiz Smart LED from your terminal!

## How to use?
* Make sure your device is on the same network as your Philips light.
* Find out the IP address of the light by going to your router's IP address.

```python
from wiz import Light

IP = '192.168.31.170'  # replace with your Wiz's IP address

light =  Light(IP)
light.off()
light.on()

light.dim(25)  # set brightness to 25%
light.dim(50)  # set brightness to 50%

light.color(colour='red')  # set colour to red using string
light.color(red=0, blue=255, green=0)  # set colour to blue using RGB values
light.color(hex='00ff00')  # set colour to green using hexcode
```
