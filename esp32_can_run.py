import os
from utils import  *
from machine import Pin, SoftI2C, I2S
from ssd1306 import SSD1306_I2C
import network, socket, uasyncio as asyncio
import urequests, ustruct
import time
import asyncio
import network
import ssl

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)  #Init i2c
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

# decode url
def unquote(s):
    res = ''
    i = 0
    while i < len(s):
        if s[i] == '%':
            if i + 2 < len(s):
                hex_value = s[i+1:i+3]
                try:
                    res += chr(int(hex_value, 16))
                    i += 3
                except ValueError:
                    res += '%'
                    i += 1
            else:
                res += '%'
                i += 1
        elif s[i] == '+':
            res += ' '
            i += 1
        else:
            res += s[i]
            i += 1
    return res

# connect wifi
def connect_wifi(ssid, password, retries=10):
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

def display_text(text, x, y):
    global oled
    if oled:
        oled.fill(0)
        oled.text(text, x, y)
        oled.show()
        time.sleep(1)

def light(rate):
    # 建立串列, 依序儲存 gpio14、gpio12、gpio13、gpio27、gpio26 腳位編號
    led_pins = [26, 27, 14, 12, 13]
    leds = [Pin(pin, Pin.OUT) for pin in led_pins]

    # 各區間對應的 LED（0-100 分成 5 個區間）
    rate_check = [[0, 20], [21, 40], [41, 60], [61, 80], [81, 100]]

    # 先全部熄滅
    for led in leds:
        led.off()

    # 根據比率決定要亮哪一顆燈
    for i, (low, high) in enumerate(rate_check):
        print(rate, str(low), str(high))
        if str(low) in rate or str(high )in rate:
            leds[4-i].on()
            break

def main():
    connect_wifi("hahahahahahahahahahahaha", "1234567890987654321")
    time.sleep(1)
    display_text("wifi connect", 0, 0)
    while True:
        asyncio.run(web_server())

async def web_server():
    addr = socket.getaddrinfo('172.25.26.193', 80)[0][-1]
    s = socket.socket()
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)  # ✅ 應該看到這行

    while True:
        cl, addr = s.accept()
        req = cl.recv(1024).decode('utf-8')
        # 只處理 POST /data
        if req.startswith('POST /bmp'):
            # 分割 header 與 body
            parts = req.split('\r\n\r\n', 1)
            if len(parts) > 1:
                body = parts[1]
                # 簡易 parse form-data (a=1&b=2)
                params = {}
                for pair in body.split('&'):
                    k, v = pair.split('=')
                    # URL decode
                    params[k] = unquote(v)
                # 擷取欄位
                img_url = params.get('url')
                level   = params.get('result')
                percent = params.get('per')

                print("Received on ESP32:", img_url, level, percent)
                if img_url and level and percent:
                    light(percent)
                    global oled
                    oled.fill(0)
                    oled.text(level, 0, 0)
                    oled.text(percent, 0, 40)
                    oled.show()
                    time.sleep(5)
                    oled.fill(0)
                    print("Downloading image...")
                    response = urequests.get(img_url)
                    bmp = response.content
                    response.close()
                    # BMP 標頭資訊
                    data_offset = int.from_bytes(bmp[10:14], 'little')
                    width = int.from_bytes(bmp[18:22], 'little')
                    height = int.from_bytes(bmp[22:26], 'little')
                    bpp = int.from_bytes(bmp[28:30], 'little')

                    if width != 128 or height != 64 or bpp != 1:
                        print("Unsupported BMP format. Must be 128x64 1-bit.")
                        return

                    row_size = ((width + 31) // 32) * 4  # BMP 每行四位元對齊

                    # 解析並顯示像素（從下到上）
                    for y in range(height):
                        row = bmp[data_offset + (height - 1 - y) * row_size : data_offset + (height - y) * row_size]
                        for x in range(width):
                            byte_index = x // 8
                            bit_index = 7 - (x % 8)
                            bit = (row[byte_index] >> bit_index) & 1
                            oled.pixel(x, y, bit)
                        oled.show()
                    print("Image displayed.")
                    
                    time.sleep(10)
                    oled.fill(0)
                    break
                elif img_url:
                    global oled
                    print("Downloading image...")
                    response = urequests.get(img_url)
                    bmp = response.content
                    response.close()
                    # BMP 標頭資訊
                    data_offset = int.from_bytes(bmp[10:14], 'little')
                    width = int.from_bytes(bmp[18:22], 'little')
                    height = int.from_bytes(bmp[22:26], 'little')
                    bpp = int.from_bytes(bmp[28:30], 'little')

                    if width != 128 or height != 64 or bpp != 1:
                        print("Unsupported BMP format. Must be 128x64 1-bit.")
                        return

                    row_size = ((width + 31) // 32) * 4  # BMP 每行四位元對齊

                    # 解析並顯示像素（從下到上）
                    for y in range(height):
                        row = bmp[data_offset + (height - 1 - y) * row_size : data_offset + (height - y) * row_size]
                        for x in range(width):
                            byte_index = x // 8
                            bit_index = 7 - (x % 8)
                            bit = (row[byte_index] >> bit_index) & 1
                            oled.pixel(x, y, bit)
                        oled.show()
                    print("Image displayed.")
                    break
                # 顯示在 OLED（或你要的動作）
                else: 
                    display_text(f"{percent}\n{level}")
                    break
                # 回應 OK
                cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK")
        cl.close()

if __name__ == '__main__':
    asyncio.run(main())

