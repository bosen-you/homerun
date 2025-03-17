import matplotlib.pyplot as plt
import numpy as np

# waveform
def plot_waveform(original_audio, modified_audio, rate, title, s, save_path=None):
    #get mininum length of two wave
    min_length = min(len(original_audio), len(modified_audio)) 
    original_audio = original_audio[:min_length]
    modified_audio = modified_audio[:min_length]
    time = np.linspace(0, min_length / rate, num=min_length)

    #picture
    plt.figure(figsize=(12, 6)) #set picture size 12*6
    plt.subplot(2, 1, 1) #set the first picture at (2, 1) (up)
    plt.plot(time, original_audio, label="Original") #import data into picture
    plt.title(f"{title} - Original") #set title 
    plt.xlabel("Time (s)") #set x-asis label
    plt.ylabel("Amplitude") #set y-asis label

    plt.subplot(2, 1, 2) #set the second picture at (2, 1) (down)
    plt.plot(time, modified_audio, label="Modified", color='red' if s == "encode" else 'blue') #import data and condtion to choose color
    plt.title(f"{title} - {'Encoded' if s == 'encode' else 'Decoded'}")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout() #auto typesetting picture

    # save picture in save_path
    if save_path:
        plt.savefig(save_path)  
    plt.show()  
    plt.close()

#frequency_spectrum
def plot_frequency_spectrum(audio, rate, title, save_path=None):
    audio = audio.flatten() # audio change to one-dimensional array
    N = len(audio) 
    yf = np.fft.fft(audio) # audio by Fast Fourier Transform, it's a y-axis frequency
    xf = np.fft.fftfreq(N, 1 / rate)[:N // 2] #because audio is symmetry, it's can take half in x-asis

    plt.figure(figsize=(10, 4)) 
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title(f"{title} - Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid() #remove background

    if save_path:
        plt.savefig(save_path) 
    plt.show()  
    plt.close()
