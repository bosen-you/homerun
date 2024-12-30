"""
實作不同的嵌入方法，例如在頻域中嵌入水印，以提高抗干擾能力
說明:
1.不同的嵌入方法：embed_watermark_frequency 函數在頻域中嵌入水印。首先讀取音頻文件，
  將水印轉換為二進制數組，然後將音頻信號轉換到頻域，將水印嵌入到頻域信號中，最後將音頻信號轉換回時域並保存。
2.提取水印：extract_watermark 和 extract_watermark_frequency 函數從音頻信號中提取數位水印。
  首先讀取音頻文件，提取音頻信號的最低有效位或頻域信號，然後將二進制數組轉換為字符串，得到提取的水印。
"""
import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, ifft

# 在頻域中嵌入水印
def embed_watermark_frequency(audio_path, watermark, output_path):
    # 讀取音頻文件
    rate, audio = wavfile.read(audio_path)
    audio = audio.astype(np.float32)

    # 將水印轉換為二進制數組
    watermark_bits = ''.join(format(ord(char), '08b') for char in watermark)

    # 將音頻信號轉換到頻域
    audio_fft = fft(audio)

    # 嵌入水印
    for i, bit in enumerate(watermark_bits):
        audio_fft[i] = audio_fft[i] * (1 + 0.01 * int(bit))

    # 將音頻信號轉換回時域
    audio_ifft = ifft(audio_fft).real

    # 保存嵌入水印的音頻文件
    wavfile.write(output_path, rate, audio_ifft.astype(np.int16))

# 提取頻域中的水印
def extract_watermark_frequency(audio_path, watermark_length):
    # 讀取音頻文件
    rate, audio = wavfile.read(audio_path)
    audio = audio.astype(np.float32)

    # 將音頻信號轉換到頻域
    audio_fft = fft(audio)

    # 提取水印
    watermark_bits = ''
    for i in range(watermark_length * 8):
        bit = 1 if abs(audio_fft[i]) > abs(audio_fft[i] / (1 + 0.01)) else 0
        watermark_bits += str(bit)

    # 將二進制數組轉換為字符串
    watermark = ''.join(chr(int(watermark_bits[i:i+8], 2)) for i in range(0, len(watermark_bits), 8))
    return watermark

# 測試嵌入和提取水印
audio_path = 'input.wav'
watermark = 'HiddenWatermark'
output_path = 'output_frequency.wav'

embed_watermark_frequency(audio_path, watermark, output_path)
extracted_watermark = extract_watermark_frequency(output_path, len(watermark))

print(f'嵌入的水印: {watermark}')
print(f'提取的水印: {extracted_watermark}')
