from machine import Pin, I2C, I2S, SPI
from ssd1306 import SSD1306_I2C
import machine
import os
import sdcard
import network
import time

class DeviceManager:
    def __init__(self):
        self.init_i2c()
        #self.init_i2s()
        self.init_sd()
        # 初始化 LED
        try:
            self.led_pins = [Pin(n, Pin.OUT) for n in (4, 12, 13, 16, 17)]
        except Exception as e:
            print("❌ LED 初始化失敗:", e)
            self.led_pins = []
        

    def init_sd(self, retries=10):
        try:
            spi = SPI(1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
            print(1-1)
            cs = Pin(15, Pin.OUT)
            print(1-2)
            sd = sdcard.SDCard(spi, cs)
            print(1-3)
            vfs = os.VfsFat(sd)
            os.mount(vfs, "/sd")
            print(1-4)
            print("✅ SD 卡初始化成功")
            self.display_text("SD 初始化成功")
            self.sd_ready = True
        except Exception as e:
            print("❌ SD 卡初始化失敗:", e)
            self.display_text("SD 初始化失敗")
            self.sd_ready = False
    
    def connect_wifi(self, ssid, password, retries=10):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.disconnect()  # 確保是重新連線
        time.sleep(1)
        wlan.connect(ssid, password)

        for i in range(10):
            if wlan.isconnected():
                print("Connected:", wlan.ifconfig())
                return
            print("Connecting...")
            time.sleep(1)

        raise RuntimeError("WiFi connection failed.")
            
    def init_i2c(self):
        # I2C 初始化 (OLED)
        try:
            i2c = I2C(0, scl=Pin(22), sda=Pin(21))
            oled = SSD1306_I2C(128, 64, i2c)
            print("✅ OLED 初始化成功")
        except Exception as e:
            print("❌ OLED 初始化失敗:", e)
            
    def init_i2s(self):
        # I2S 初始化
        try:
            self.audio_in = I2S(
                0,
                sck=Pin(32),
                ws=Pin(25),
                sd=Pin(33),
                mode=I2S.RX,
                bits=32,
                format=I2S.MONO,
                rate=16000,
                ibuf=20000
            )
            self.audio_out = I2S(
                1,  # 注意要用不同 I2S 編號
                sck=Pin(26),
                ws=Pin(25),
                sd=Pin(27),
                mode=I2S.TX,
                bits=16,
                format=I2S.MONO,
                rate=44100,
                ibuf=20000
            )
            print("✅ I2S 初始化成功")
        except Exception as e:
            print("❌ I2S 初始化失敗:", e)
            self.audio_in = None
            self.audio_out = None
            
    def display_text(self, text, x=0, y=0):
        if self.oled:
            self.oled.fill(0)
            self.oled.text(text, x, y)
            self.oled.show()
            time.sleep(1)
            
