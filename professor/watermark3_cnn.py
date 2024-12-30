# 使用 TensorFlow 來訓練一個卷積神經網絡（CNN）模型，用於嵌入和提取水印。
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv1D, Conv1DTranspose
from tensorflow.keras.models import Model
from scipy.io import wavfile

# 讀取音頻文件
rate, audio = wavfile.read('dream1.wav')
audio = audio.astype(np.float32) / 32768.0  # 正規化

# 確保音頻數據的形狀與模型預期的形狀一致
if len(audio.shape) == 2:
    audio = audio[:, 0]  # 取第一個聲道
audio = np.expand_dims(audio, axis=-1)
audio = np.expand_dims(audio, axis=0)

# 定義卷積神經網絡模型
input_audio = Input(shape=(audio.shape[1], 1))
x = Conv1D(16, 3, activation='relu', padding='same')(input_audio)
x = Conv1D(8, 3, activation='relu', padding='same')(x)
encoded = Conv1D(8, 3, activation='relu', padding='same')(x)
x = Conv1DTranspose(8, 3, activation='relu', padding='same')(encoded)
x = Conv1DTranspose(16, 3, activation='relu', padding='same')(x)
decoded = Conv1DTranspose(1, 3, activation='sigmoid', padding='same')(x)

autoencoder = Model(input_audio, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# 訓練模型
autoencoder.fit(audio, audio, epochs=50, batch_size=1)

# 保存模型
autoencoder.save('audio_autoencoder1.h5')


# 使用訓練好的卷積神經網絡模型來嵌入水印。
from tensorflow.keras.models import load_model

# 加載模型
autoencoder = load_model('audio_autoencoder1.h5')

# 將水印轉換為二進制數組
watermark = 'HiddenWatermark_cnn'
watermark_bits = ''.join(format(ord(char), '08b') for char in watermark)

# 嵌入水印
encoded_audio = autoencoder.predict(audio)
encoded_audio = encoded_audio.flatten()
encoded_audio = (encoded_audio * 32768).astype(np.int16)  # 確保數據類型為整數
for i, bit in enumerate(watermark_bits):
    encoded_audio[i] = (encoded_audio[i] & ~1) | int(bit)

# 保存嵌入水印的音頻文件
encoded_audio = encoded_audio.reshape(-1, 1)
wavfile.write('output_with_watermark1.wav', rate, encoded_audio)
print(f'嵌入的水印: {watermark}',', 檔名:output_with_watermark1.wav')


# 使用訓練好的卷積神經網絡模型來提取水印。
# 提取水印
def extract_watermark(encoded_audio, watermark_length):
    encoded_audio = encoded_audio.flatten()
    watermark_bits = ''
    for i in range(watermark_length * 8):
        watermark_bits += str(int(encoded_audio[i] & 1))
    
    watermark = ''.join(chr(int(watermark_bits[i:i+8], 2)) for i in range(0, len(watermark_bits), 8))
    return watermark

# 提取水印
extracted_watermark = extract_watermark(encoded_audio, len(watermark))
print(f'提取的水印: {extracted_watermark}')
