import os
import numpy as np
from scipy.io import wavfile
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog

# select audio in flie
def select_audio_file():
    app = QApplication(sys.argv) #initially
    file_path, _ = QFileDialog.getOpenFileName( #file_path, filter
        None, #parent
        "選擇音頻文件", # caption 
        "", # directory
        "WAV files (*.wav);;All files (*.*)" # filter
    )

    if file_path:
        print(f"已選擇文件: {file_path}")
    else:
        print("未選擇任何文件")
        exit(1)

    # 
    if not os.path.isfile(file_path):
            print("音頻文件無效，請檢查文件路徑！")
            exit(1)

    # audio to hex
    rate, audio = wavfile.read(file_path)   
    if audio.dtype != np.int16:
        audio = audio.astype(np.int16)
    desktop_path = os.path.join(os.path.expanduser("~"), "watermark")

    # determine whether file exist
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    return rate, audio, desktop_path


def select_audio_file_path():
    app = QApplication(sys.argv)  
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "選擇音頻文件",
        "",
        "WAV files (*.wav);;All files (*.*)"
    )

    if file_path:
        print(f"已選擇文件: {file_path}")
    else:
        print("未選擇任何文件")
        exit(1)

    if not os.path.isfile(file_path):
            print("音頻文件無效，請檢查文件路徑！")
            exit(1)
    return file_path
