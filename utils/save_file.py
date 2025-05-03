import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
import wave
import io
from db import session, Static
from cloudinary_config import cloudinary
import cloudinary.uploader

def save_photo():
    # 將 plt 直接儲存到 BytesIO 中
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # 上傳 png 圖片
    result_png = cloudinary.uploader.upload(buf, resource_type="image", public_id=f"waveform_{datetime.now().timestamp()}")
    png_url = result_png["secure_url"]

    # 轉為灰階並進行 BMP 轉換
    buf.seek(0)
    img = Image.open(buf).convert("L").resize((128, 64))
    threshold = 128
    img = img.point(lambda x: 255 if x > threshold else 0, mode='1')

    bmp_buf = io.BytesIO()
    img.save(bmp_buf, format='BMP')
    bmp_buf.seek(0)

    result_bmp = cloudinary.uploader.upload(bmp_buf, resource_type="image", public_id=f"bmp_{datetime.now().timestamp()}")
    bmp_url = result_bmp["secure_url"]

    # 儲存到資料庫
    upload_image = [Static(filename=png_url), Static(filename=bmp_url)]
    session.add_all(upload_image)
    session.commit()

    return png_url, bmp_url


def save_audio(audio, rate, num_channels=1, sample_width=2):
    # 將 audio 儲存到 BytesIO
    audio_buf = io.BytesIO()
    with wave.open(audio_buf, "wb") as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(audio)
    audio_buf.seek(0)

    # 上傳到 Cloudinary
    result_audio = cloudinary.uploader.upload(audio_buf, resource_type="video", public_id=f"audio_{datetime.now().timestamp()}")
    audio_url = result_audio["secure_url"]

    # 存入資料庫
    session.add(Static(filename=audio_url))
    session.commit()

    return audio_url