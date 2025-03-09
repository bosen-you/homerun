import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import resample 
import os

def plot_audio_comparison(rate1, audio1, desktop_path, audio2):
    """ 使用選擇的音檔，繪製波形與頻譜比較圖 """
    save_path = os.path.join(desktop_path, "comparison.png")

    # 轉換為單聲道
    if len(audio1.shape) > 1:
        audio1 = audio1.mean(axis=1).astype(np.int16)
    if len(audio2.shape) > 1:
        audio2 = audio2.mean(axis=1).astype(np.int16)

    # 讓兩個音檔長度相同
    min_length = min(len(audio1), len(audio2))
    audio1, audio2 = audio1[:min_length], audio2[:min_length]

    # 計算時間軸
    time = np.linspace(0, min_length / rate1, num=min_length)

    # 計算 FFT 頻譜
    fft1 = np.fft.fft(audio1)
    fft2 = np.fft.fft(audio2)
    freqs = np.fft.fftfreq(min_length, 1 / rate1)[:min_length // 2]

    # 繪製比較圖
    plt.figure(figsize=(12, 8))

    # 波形比較
    plt.subplot(2, 1, 1)
    plt.plot(time, audio1, label="音檔 1", alpha=0.7)
    plt.plot(time, audio2, label="音檔 2", alpha=0.7)
    plt.title("波形比較")
    plt.xlabel("時間 (秒)")
    plt.ylabel("振幅")
    plt.legend()

    # 頻譜比較
    plt.subplot(2, 1, 2)
    plt.plot(freqs, np.abs(fft1[:min_length // 2]), label="音檔 1 頻譜", alpha=0.7)
    plt.plot(freqs, np.abs(fft2[:min_length // 2]), label="音檔 2 頻譜", alpha=0.7)
    plt.title("頻譜比較")
    plt.xlabel("頻率 (Hz)")
    plt.ylabel("振幅")
    plt.legend()

    plt.tight_layout()

    # 存檔
    plt.savefig(save_path)
    print(f"比較結果已儲存到: {save_path}")

    plt.show()
