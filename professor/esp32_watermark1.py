"""
說明:
1.嵌入水印：embed_watermark 函數將數位水印嵌入到音頻信號中。首先將水印轉換為二進制數組，然後將水印嵌入到音頻信號的最低有效位（LSB）中。
2.讀取音頻信號：read_audio 函數從 ADC 讀取音頻信號。
3.播放音頻信號：play_audio 函數使用 DAC 播放音頻信號。
4.提取水印：extract_watermark 函數從音頻信號中提取數位水印。首先提取音頻信號的最低有效位，然後將二進制數組轉換為字符串，得到提取的水印。
"""
import machine
import ustruct
import uarray

# 初始化 ADC 和 DAC
adc = machine.ADC(machine.Pin(36))
dac = machine.DAC(machine.Pin(25))

# 嵌入水印
def embed_watermark(audio, watermark):
    watermark_bits = ''.join(format(ord(char), '08b') for char in watermark)
    audio_with_watermark = uarray.array('h', audio)
    
    for i, bit in enumerate(watermark_bits):
        audio_with_watermark[i] = (audio_with_watermark[i] & ~1) | int(bit)
    
    return audio_with_watermark

# 讀取音頻信號
def read_audio():
    audio = []
    for _ in range(1000):  # 假設讀取 1000 個樣本
        audio.append(adc.read())
    return audio

# 播放音頻信號
def play_audio(audio):
    for sample in audio:
        dac.write(sample)

# 提取水印
def extract_watermark(audio, watermark_length):
    watermark_bits = ''
    for i in range(watermark_length * 8):
        watermark_bits += str(audio[i] & 1)
    
    watermark = ''.join(chr(int(watermark_bits[i:i+8], 2)) for i in range(0, len(watermark_bits), 8))
    return watermark

# 嵌入和播放水印音頻
audio = read_audio()
watermark = "HiddenWatermark"
audio_with_watermark = embed_watermark(audio, watermark)
play_audio(audio_with_watermark)

# 提取水印
extracted_watermark = extract_watermark(audio_with_watermark, len(watermark))
print(f'提取的水印: {extracted_watermark}')
