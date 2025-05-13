# main.py
from microdot import Microdot, Response
import os

app = Microdot()
Response.default_content_type = 'text/plain'

UPLOAD_FOLDER = '/upload'  # ESP32 上的儲存路徑

@app.post('/upload')
async def upload(request):
    file = request.files.get('file')
    if file:
        filename = file.filename or 'result.jpg'
        file_path = f"{UPLOAD_FOLDER}/{filename}"
        with open(file_path, 'wb') as f:
            f.write(file.read())
        print(f"圖片已儲存至 {file_path}")
        return '圖片上傳成功', 200
    else:
        return '沒有接收到圖片', 400

@app.get('/')
def index(request):
    return 'ESP32 圖片上傳伺服器啟動中'

app.run()

