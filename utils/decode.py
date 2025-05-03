import numpy as np
from scipy.signal import resample
# extract watermark
def extract_watermark(audio, watermark_length=32):
    audio = audio.flatten()
    # LSB
    watermark_bits = ''.join(str(audio[i] & 1) for i in range(watermark_length))
    encryption_id = ''.join(hex(int(watermark_bits[i:i + 4], 2))[2:].upper() for i in range(0, len(watermark_bits), 4))
    return encryption_id

# remove watermark
def remove_watermark(audio, watermark_length=32):
    audio = audio.copy().flatten()
    for i in range(watermark_length):
        audio[i] = audio[i] & ~1
    return speed_up_audio(audio)

# speed up audio
def speed_up_audio(audio, speed_factor=2.0):
    num_samples = int(len(audio) / speed_factor)
    resampled_audio = resample(audio, num_samples) # resampling the audio
    # clips the resampled audio values to fit within the range of 16-bit signed integers, which is the typical range for audio samples.
    resampled_audio = np.clip(resampled_audio, -32768, 32767).astype(np.int16)

    return resampled_audio