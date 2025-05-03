import cloudinary
import cloudinary.uploader
from urllib.parse import urlparse
from datetime import datetime, timedelta
from db import session, Static
import schedule
import time
import threading

def extract_url(url):
    path = urlparse(url).path
    parts = path.split('/')
    file = parts[-1].rsplit(".")
    print(file)
    filename = f'{file[0]}.{file[1]}'
    return filename

def delete_public_url():
    expiration_time = datetime.now() - timedelta(hours=3)
    expired_file = session.query(Static).filter(Static.timestamp < expiration_time).all()

    print(expired_file)
    for file in expired_file:
        url = file.filename
        if "res.cloudinary.com" in url:
            public_id = extract_url(url)
            resource_type = "video" if url.endswith(".wav") else "image"

            try:
                result = cloudinary.uploader.destroy(public_id)
                print(f"✅ 刪除 Cloudinary 檔案：{public_id}")
                #session.delete(file)
            except Exception as e:
                print(f"❌ Cloudinary 刪除失敗：{e}")
        #else:
            #session.delete(file)

    session.commit()
    print("🧹 過期檔案清理完成。")

def run_scheduled_tasks():
    # 每天凌晨 3 點清理一次
    schedule.every().day.at("15:29").do(delete_public_url)
    while True:
        schedule.run_pending()
        time.sleep(60)


def start_background_scheduler():
    scheduler_thread = threading.Thread(target=run_scheduled_tasks)
    scheduler_thread.daemon = True  # 設定為守護線程
    scheduler_thread.start()
