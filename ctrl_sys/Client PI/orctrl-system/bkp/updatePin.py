from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep

pin = port.PG7
print pin

gpio.init()
gpio.setcfg(pin, gpio.OUTPUT)
gpio.output(pin, 0)	
sleep(2)	














