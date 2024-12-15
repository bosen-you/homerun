"""
>pip3 install numpy scipy pydub
這個範例展示了如何使用 Python 和 AI 技術來實作聲音隱藏式浮水印。
說明:
1.確保音頻數據是整數類型：在讀取音頻文件後，檢查 audio 數組的數據類型，如果不是 np.int16，則將其轉換為 np.int16。
2.展平音頻數據：將音頻數據展平為一維數組，這樣可以確保 audio[i] 是單個值。
3.嵌入水印：embed_watermark 函數將數位水印嵌入到音頻信號中。首先讀取音頻文件，將水印轉換為二進制數組，然後將水印嵌入到音頻信號的最低有效位（LSB）中，最後保存嵌入水印的音頻文件。
4.重新調整音頻數據形狀：將音頻數據重新調整為原始形狀，這樣可以確保音頻文件的格式正確。
5.提取水印：extract_watermark 函數從音頻信號中提取數位水印。首先讀取音頻文件，提取音頻信號的最低有效位，然後將二進制數組轉換為字符串，得到提取的水印。
6.測試嵌入和提取水印：測試嵌入和提取水印的功能，並打印嵌入和提取的水印。
"""
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment

# 嵌入水印
def embed_watermark(audio_path, watermark, output_path):
    # 讀取音頻文件
    rate, audio = wavfile.read(audio_path)
    
    # 確保音頻數據是整數類型
    if audio.dtype != np.int16:
        audio = audio.astype(np.int16)

    # 將音頻數據展平為一維數組
    audio = audio.flatten()

    # 將水印轉換為二進制數組
    watermark_bits = ''.join(format(ord(char), '08b') for char in watermark)

    # 嵌入水印
    for i, bit in enumerate(watermark_bits):
        audio[i] = (audio[i] & ~1) | int(bit)

    # 將音頻數據重新調整為原始形狀
    audio = audio.reshape(-1, 2)

    # 保存嵌入水印的音頻文件
    wavfile.write(output_path, rate, audio)

# 提取水印
def extract_watermark(audio_path, watermark_length):
    # 讀取音頻文件
    rate, audio = wavfile.read(audio_path)
    
    # 確保音頻數據是整數類型
    if audio.dtype != np.int16:
        audio = audio.astype(np.int16)

    # 將音頻數據展平為一維數組
    audio = audio.flatten()

    # 提取水印
    watermark_bits = ''
    for i in range(watermark_length * 8):
        watermark_bits += str(int(audio[i] & 1))

    # 將二進制數組轉換為字符串
    watermark = ''.join(chr(int(watermark_bits[i:i+8], 2)) for i in range(0, len(watermark_bits), 8))
    return watermark

# 測試嵌入和提取水印
audio_path = 'dream1.wav'
watermark  = 'HiddenWatermark_test'
output_path= 'output1.wav'

embed_watermark(audio_path, watermark, output_path)
extracted_watermark = extract_watermark(output_path, len(watermark))

print(f'嵌入的水印: {watermark}')
print(f'提取的水印: {extracted_watermark}')
