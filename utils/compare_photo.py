import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 設定取樣率
SR = 44100  # 取樣率（音樂 22050 / 語音 16000）

# 讀取音檔
def load_audio(file_path, sr=SR):
    y, sr = librosa.load(file_path, sr=sr)
    return y, sr

# 繪製波形圖
def plot_waveform(audio_path1, audio_path2):
    y1, sr1 = load_audio(audio_path1)
    y2, sr2 = load_audio(audio_path2)

    plt.figure(figsize=(12, 4))

    # 第一個音檔
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y1, sr=sr1, alpha=0.7)
    plt.title("Waveform - Audio 1")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # 第二個音檔
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(y2, sr=sr2, alpha=0.7, color="orange")
    plt.title("Waveform - Audio 2")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()

# 繪製頻譜圖
def plot_spectrogram(audio_path1, audio_path2):
    y1, sr1 = load_audio(audio_path1)
    y2, sr2 = load_audio(audio_path2)

    plt.figure(figsize=(12, 6))

    # 第一個音檔
    plt.subplot(2, 1, 1)
    D1 = librosa.amplitude_to_db(np.abs(librosa.stft(y1)), ref=np.max)
    librosa.display.specshow(D1, sr=sr1, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram - Audio 1")

    # 第二個音檔
    plt.subplot(2, 1, 2)
    D2 = librosa.amplitude_to_db(np.abs(librosa.stft(y2)), ref=np.max)
    librosa.display.specshow(D2, sr=sr2, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram - Audio 2")

    plt.tight_layout()
    plt.show()


