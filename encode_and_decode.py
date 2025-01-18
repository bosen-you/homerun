import os
import numpy as np
import random
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt 

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

    # 計算 XOR 結果
    ba_xor_A = bytes_xor_to_hexstring(bytes.fromhex(A1), bytes.fromhex(A2))
    ba_xor_B = bytes_xor_to_hexstring(bytes.fromhex(B1), bytes.fromhex(B2))

    # 將兩個 8 位壓縮為 8 位
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

# 提取加密標識
def extract_watermark(audio, watermark_length=32):
    audio = audio.flatten()
    watermark_bits = ''.join(str(audio[i] & 1) for i in range(watermark_length))
    encryption_id = ''.join(
        hex(int(watermark_bits[i:i + 4], 2))[2:].upper() for i in range(0, len(watermark_bits), 4)
    )
    return encryption_id

# 移除加密標識
def remove_watermark(audio, watermark_length=32):
    audio = audio.copy().flatten()
    for i in range(watermark_length):
        audio[i] = audio[i] & ~1
    return audio

# 將音訊加速 2 倍（即兩倍速）
def speed_up_audio(audio, rate, speed_factor=2.0):
    num_samples = int(len(audio) / speed_factor)
    resampled_audio = signal.resample(audio, num_samples)
    resampled_audio = np.clip(resampled_audio, -32768, 32767).astype(np.int16)
    return resampled_audio

# 繪製波形圖
# 繪製波形圖
def plot_waveform(original_audio, modified_audio, rate, title, s):
    # 確保原始和修改後音訊的數據長度一致
    min_length = min(len(original_audio), len(modified_audio))
    original_audio = original_audio[:min_length]
    modified_audio = modified_audio[:min_length]
    
    time = np.linspace(0, min_length / rate, num=min_length)
    
    if s == "encode":
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(time, original_audio, label="Original")
        plt.title(f"{title} - Original")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
    
        plt.subplot(2, 1, 2)
        plt.plot(time, modified_audio, label="Modified", color='orange')
        plt.title(f"{title} - encoded")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        
        plt.tight_layout()
        plt.show()
    else:
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(time, original_audio, label="Original")
        plt.title(f"{title} - encoded")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")

        plt.subplot(2, 1, 2)
        plt.plot(time, modified_audio, label="Modified", color='blue')
        plt.title(f"{title} - decoded")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        
        plt.tight_layout()
        plt.show()


# 主程序
if __name__ == "__main__":
    try:
        audio_path = input("請輸入音頻檔案的絕對路徑: ").strip()
        if not os.path.isfile(audio_path):
            print("音頻文件無效，請檢查文件路徑！")
            exit(1)

        rate, audio = wavfile.read(audio_path)
        if audio.dtype != np.int16:
            audio = audio.astype(np .int16)

        # 動態獲取桌面路徑
        desktop_path = os.path.join(os.path.expanduser("~"), "watermark")

        # 確保目標文件夾存在
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)


        action = input("輸入 'encode' 進行加密，輸入 'decode' 進行解密: ").lower()

        if action == "encode":
            encryption_id = generate_encryption_id()
            encoded_audio = embed_watermark(audio, encryption_id)
            output_name = input("請輸入加密後檔案的名稱: ")
            speeded_audio = speed_up_audio(encoded_audio, rate)
            output_path = os.path.join(desktop_path, f"{output_name}_{encryption_id}.wav")
            wavfile.write(output_path, rate, speeded_audio)
            print(f"嵌入完成，結果已保存至: {output_path}")
            plot_waveform(audio, speeded_audio, rate, "Wave form Watermark", "encode")

        elif action == "decode":
            extracted_id = extract_watermark(audio)
            #print(f"提取的密鑰為: {extracted_id}")
            psw = input("請輸入密鑰進行驗證: ")

            if psw == extracted_id:
                psw = input("是否移除水印並生成解密後音檔？(y/n): ").lower() == 'y'
                if psw:
                    speeded_audio = speed_up_audio(audio, rate)
                    output_name = input("請輸入解密後檔案的名稱: ")
                    output_path = os.path.join(desktop_path, f"{output_name}_watermark_removed.wav")
                    wavfile.write(output_path, rate, speeded_audio)
                    print(f"水印已移除，解密後的音頻已保存至: {output_path}")
                    plot_waveform(audio, speeded_audio, rate, "Waveform with Watermark", "decode")
            else:
                print("密鑰錯誤！操作中止。")

        else:
            print("無效選項，請重新執行程式！")
    except Exception as e:
        print(f"程式執行錯誤: {e}")
