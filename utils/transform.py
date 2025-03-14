import matplotlib.pyplot as plt
import numpy as np

# 波形圖
def plot_waveform(original_audio, modified_audio, rate, title, s, save_path=None):
    #讓兩音檔長度相同
    min_length = min(len(original_audio), len(modified_audio)) 
    original_audio = original_audio[:min_length]
    modified_audio = modified_audio[:min_length]
    time = np.linspace(0, min_length / rate, num=min_length) #建立time陣列，表示音訊時間軸

    
    plt.figure(figsize=(12, 6)) #設定圖大小(12 inchs * 8 inchs)
    plt.subplot(2, 1, 1) #建立2行*列1的子圖
    plt.plot(time, original_audio, label="Original") #劃出波型
    plt.title(f"{title} - Original") #大標
    plt.xlabel("Time (s)") #x小標
    plt.ylabel("Amplitude") #y小標

    plt.subplot(2, 1, 2)
    plt.plot(time, modified_audio, label="Modified", color='red' if s == "encode" else 'blue')
    plt.title(f"{title} - {'Encoded' if s == 'encode' else 'Decoded'}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout() #自動調整間距

    if save_path:
        plt.savefig(save_path)  
    plt.show()  #顯示圖片
    plt.close() #關閉圖片

#頻率圖
def plot_frequency_spectrum(audio, rate, title, save_path=None):
    audio = audio.flatten()
    N = len(audio)
    yf = np.fft.fft(audio) #傅立葉轉換
    xf = np.fft.fftfreq(N, 1 / rate)[:N // 2] #傅立葉轉換會前後對稱 -> 取一半

    plt.figure(figsize=(10, 4))
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title(f"{title} - Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid() #使用網格線 初始：True

    if save_path:
        plt.savefig(save_path) #存圖片到絕對路徑
    plt.show()  
    plt.close()
