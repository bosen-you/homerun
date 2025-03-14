import os
import numpy as np
from scipy.io import wavfile
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog

def select_audio_file():
    app = QApplication(sys.argv)  #初始化GUI介面
    file_path, _ = QFileDialog.getOpenFileName(
        None, #沒有父視窗
        "選擇音頻文件", #對話框標題
        "", #預設路徑
        "WAV files (*.wav);;All files (*.*)" #接受檔案格式
    )

    if file_path:
        print(f"已選擇文件: {file_path}")
    else:
        print("未選擇任何文件")
        exit(1)

    if not os.path.isfile(file_path):
            print("音頻文件無效，請檢查文件路徑！")
            exit(1)

    rate, audio = wavfile.read(file_path)   
    if audio.dtype != np.int16:
        audio = audio.astype(np.int16)
    desktop_path = os.path.join(os.path.expanduser("~"), "watermark") #獲取用戶名 ex: C:\User\user\bosenda\watermark

    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    return rate, audio, desktop_path
