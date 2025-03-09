import random
from scipy.signal import resample
import numpy as np
# 隨機生成 8 位十六進位字串
def generate_random_hex_string():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(8))

# XOR 運算並返回十六進位字串
def bytes_xor_to_hexstring(ba1, ba2):
    return bytes([a ^ b for a, b in zip(ba1, ba2)]).hex()

# 生成加密標識（8 位）
def generate_encryption_id():
    A1 = generate_random_hex_string()
    A2 = generate_random_hex_string()
    B1 = generate_random_hex_string()
    B2 = generate_random_hex_string()
    ba_xor_A = bytes_xor_to_hexstring(bytes.fromhex(A1), bytes.fromhex(A2))
    ba_xor_B = bytes_xor_to_hexstring(bytes.fromhex(B1), bytes.fromhex(B2))
    final_id = bytes_xor_to_hexstring(bytes.fromhex(ba_xor_A), bytes.fromhex(ba_xor_B)).upper()
    print(f"浮水印密鑰，請妥善保存: {final_id}")
    return final_id

# 嵌入加密標識
def embed_watermark(audio, encryption_id):
    watermark_bits = ''.join(format(int(char, 16), '04b') for char in encryption_id)
    audio = audio.flatten()
    for i, bit in enumerate(watermark_bits):
        audio[i] = (audio[i] & ~1) | int(bit)
    return audio

#將音訊加速 2 倍
def speed_up_audio(audio, rate, speed_factor=2.0):
    num_samples = int(len(audio) / speed_factor)
    resampled_audio = resample(audio, num_samples)
    resampled_audio = np.clip(resampled_audio, -32768, 32767).astype(np.int16)
    return resampled_audio
