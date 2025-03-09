import matplotlib.pyplot as plt
import numpy as np

# 波形圖
def plot_waveform(original_audio, modified_audio, rate, title, s, save_path=None):
    min_length = min(len(original_audio), len(modified_audio))
    original_audio = original_audio[:min_length]
    modified_audio = modified_audio[:min_length]
    time = np.linspace(0, min_length / rate, num=min_length)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time, original_audio, label="Original")
    plt.title(f"{title} - Original")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.subplot(2, 1, 2)
    plt.plot(time, modified_audio, label="Modified", color='red' if s == "encode" else 'blue')
    plt.title(f"{title} - {'Encoded' if s == 'encode' else 'Decoded'}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)  
    plt.show()  
    plt.close()

#頻率圖
def plot_frequency_spectrum(audio, rate, title, save_path=None):
    audio = audio.flatten()
    N = len(audio)
    yf = np.fft.fft(audio)
    xf = np.fft.fftfreq(N, 1 / rate)[:N // 2]

    plt.figure(figsize=(10, 4))
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title(f"{title} - Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()

    if save_path:
        plt.savefig(save_path) 
    plt.show()  
    plt.close()

if __name__ == '__main__':
    plot_waveform()
    plot_frequency_spectrum()