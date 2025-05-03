import network 

def connect_wifi(ssid, password):
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