import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import resample 

def analyze_audio_similarity(rate1, audio1, rate2, audio2):
    """ 使用選擇的音檔，計算相似度（整數百分比） """
    # 轉換為單聲道
    if len(audio1.shape) > 1:
        audio1 = audio1.mean(axis=1).astype(np.int16)
    if len(audio2.shape) > 1:
        audio2 = audio2.mean(axis=1).astype(np.int16)

    # 讓兩個音檔的長度相同
    min_length = min(len(audio1), len(audio2))
    audio1, audio2 = audio1[:min_length], audio2[:min_length]

    # 採樣率不同，則重採樣
    if rate1 != rate2:
        print("採樣率不同，正在重採樣...")
        if rate1 > rate2:
            audio1 = resample(audio1, int(len(audio1) * rate2 / rate1))
        else:
            audio2 = resample(audio2, int(len(audio2) * rate1 / rate2))
        rate1 = rate2 = min(rate1, rate2)

    # 計算均方誤差（MSE）
    mse = np.mean((audio1 - audio2) ** 2)

    # 計算皮爾遜相關係數
    correlation = np.corrcoef(audio1, audio2)[0, 1]

    # 轉換為相似度百分比
    mse_similarity = max(0, 100 - int(mse / np.max(audio1) * 100))  # 低誤差代表高相似度
    correlation_similarity = int((correlation + 1) / 2 * 100)  # 相關係數轉換為 0-100%

    # 計算平均相似度（四捨五入）
    final_similarity = round((mse_similarity + correlation_similarity) / 2)

    return final_similarity
