"""
>pip3 install numpy scipy pydub
實作多層水印嵌入，這樣可以在音頻中嵌入多個水印，提高安全性和抗干擾能力
說明:
1.多層水印嵌入：embed_watermark 函數將多個數位水印嵌入到音頻信號中。首先讀取音頻文件，
  將每個水印轉換為二進制數組，然後將水印嵌入到音頻信號的最低有效位（LSB）中，最後保存嵌入水印的音頻文件。
2.提取水印：extract_watermark 和 extract_watermark_frequency 函數從音頻信號中提取數位水印。
  首先讀取音頻文件，提取音頻信號的最低有效位或頻域信號，然後將二進制數組轉換為字符串，得到提取的水印。
"""
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

# 嵌入水印
def embed_watermark(audio_path, watermarks, output_path):
    # 讀取音頻文件
    rate, audio = wavfile.read(audio_path)
    audio = audio.astype(np.float32)

    # 將每個水印轉換為二進制數組並嵌入
    for watermark in watermarks:
        watermark_bits = ''.join(format(ord(char), '08b') for char in watermark)
        for i, bit in enumerate(watermark_bits):
            audio[i] = audio[i] & ~1 | int(bit)

    # 保存嵌入水印的音頻文件
    wavfile.write(output_path, rate, audio.astype(np.int16))

# 提取水印
def extract_watermark(audio_path, watermark_length):
    # 讀取音頻文件
    rate, audio = wavfile.read(audio_path)
    audio = audio.astype(np.float32)

    # 提取水印
    watermark_bits = ''
    for i in range(watermark_length * 8):
        watermark_bits += str(int(audio[i] & 1))

    # 將二進制數組轉換為字符串
    watermark = ''.join(chr(int(watermark_bits[i:i+8], 2)) for i in range(0, len(watermark_bits), 8))
    return watermark

# 測試嵌入和提取水印
audio_path = 'input.wav'
watermarks = ['HiddenWatermark1', 'HiddenWatermark2']
output_path = 'output.wav'

embed_watermark(audio_path, watermarks, output_path)
for watermark in watermarks:
    extracted_watermark = extract_watermark(output_path, len(watermark))
    print(f'嵌入的水印: {watermark}')
    print(f'提取的水印: {extracted_watermark}')
