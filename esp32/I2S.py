'''
Desciption: 
    This file aims to record and play video using the I2S. 
    The recorded and played audio is automatically saved in SDcard.
Notice: 
    This code isn't currently compatible with the ESP32. 
    If you manage to modify and run it successfully on the ESP32, feel free to DM me. Thank you!
'''

from inital import DeviceManage
import ustruct
import os

def get_sd_free_bytes(path="/sd"):
    "To get sdcard maximum supported"
    stats = os.statvfs(path)
    free_bytes = stats[0] * stats[3]  # f_frsize * f_bavail
    return free_bytes

def estimate_max_duration(sample_rate=16000, bits=16, channels=1, path="/sd"):
    "Calculate the maximum recording duration based on the SD card's available storage capacity."
    bytes_per_sec = sample_rate * (bits // 8) * channels
    free_bytes = get_sd_free_bytes(path)
    return free_bytes // bytes_per_sec

def create_wav_header(sample_rate, bits_per_sample, num_channels, datasize):
    header = b'RIFF'
    header += (datasize + 36).to_bytes(4, 'little')  # ChunkSize = datasize + 36
    header += b'WAVE'
    header += b'fmt '
    header += (16).to_bytes(4, 'little')             # Subchunk1Size = 16 for PCM
    header += (1).to_bytes(2, 'little')               # AudioFormat = 1 (PCM)
    header += (num_channels).to_bytes(2, 'little')
    header += (sample_rate).to_bytes(4, 'little')
    header += (sample_rate * num_channels * bits_per_sample // 8).to_bytes(4, 'little')  # ByteRate
    header += (num_channels * bits_per_sample // 8).to_bytes(2, 'little')                # BlockAlign
    header += (bits_per_sample).to_bytes(2, 'little')
    header += b'data'
    header += (datasize).to_bytes(4, 'little')         # Subchunk2Size = datasize
    return header

async def record_wav(path, duration_s, filename):
    dev = DeviceManager()
    audio_in = dev.audio_in
    sample_rate = 16000
    buffer_size = 1024

    total_bytes = sample_rate * duration_s * 2  # 2 bytes per sample (16bit mono)

    with open(path, "wb") as f:
        f.write(wav_header(sample_rate, 16, 1, total_bytes))  # 預寫 WAV header

        remaining = total_bytes
        audio_buf = bytearray(buffer_size)

        while remaining > 0:
            num_read = audio_in.readinto(audio_buf)
            if num_read:
                f.write(audio_buf[:num_read])
                remaining -= num_read

    print(f"✅ recording successfully，saved to {full_path}")

async def play_wav(path):
    with open(path, "rb") as f:
        f.read(44)
        while True:
            buf = f.read(512)
            if not buf:
                break
            audio_out.write(buf)
