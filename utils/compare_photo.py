import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Set sampling rate
SR = 44100  # Sampling rate (music 22050 / speech 16000)

# Load audio file
def load_audio(file_path, sr=SR):
    y, sr = librosa.load(file_path, sr=sr)
    return y, sr

# Plot waveform
def plot_waveform(audio_path1, audio_path2):
    y1, sr1 = load_audio(audio_path1)
    y2, sr2 = load_audio(audio_path2)

    plt.figure(figsize=(12, 4))

    # First audio file
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y1, sr=sr1, alpha=0.7)
    plt.title("Waveform - Audio 1")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    # Second audio file
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(y2, sr=sr2, alpha=0.7, color="orange")
    plt.title("Waveform - Audio 2")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()

# Plot spectrogram
def plot_spectrogram(audio_path1, audio_path2):
    y1, sr1 = load_audio(audio_path1)
    y2, sr2 = load_audio(audio_path2)

    plt.figure(figsize=(12, 6))

    # First audio file
    plt.subplot(2, 1, 1)
    D1 = librosa.amplitude_to_db(np.abs(librosa.stft(y1)), ref=np.max)
    librosa.display.specshow(D1, sr=sr1, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram - Audio 1")

    # Second audio file
    plt.subplot(2, 1, 2)
    D2 = librosa.amplitude_to_db(np.abs(librosa.stft(y2)), ref=np.max)
    librosa.display.specshow(D2, sr=sr2, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram - Audio 2")

    plt.tight_layout()
    plt.show()
