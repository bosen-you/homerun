import urquest

def fetch_latest_image_url():
    res = urequests.get("http://172.20.10.13:8000/data")
    print("Response:", res.text)  # ← 印出原始 JSON 內容
    bmp = res.json()["url"]
    result  = res.json["result"]
    pre = res.json["per"]
    res.close()
    return bmp, result, per
