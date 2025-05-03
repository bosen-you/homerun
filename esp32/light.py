from inital import DeviceManager
from machine import Pin
import time

def light(rate):
    dev = DeviceManager()
    leds = dev.led_pins()
    
    rate_check = [[0, 20], [21, 40], [41, 60], [61, 80], [81, 100]]

    # 先全部熄滅
    for led in leds:
        led.off()

    # 根據比率決定要亮哪一顆燈
    for i, (low, high) in enumerate(rate_check):
        if low <= rate <= high:
            leds[i].on()
            break