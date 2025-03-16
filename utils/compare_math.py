import librosa
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from fastdtw import fastdtw  # 更快的 DTW
import os

# 設定 MFCC 參數
N_MFCC = 25  # 可以調低以加速運算
SR = 44100  # 降低取樣率，加快處理速度

# 預計算 MFCC 以避免重複計算
def compute_mfcc(audio_path):
    y, sr = librosa.load(audio_path, sr=SR)  # 固定取樣率
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    return np.mean(mfcc, axis=1), mfcc.T  # 回傳均值和完整 MFCC

# 快速 DTW（使用 fastdtw）
def compute_dtw(mfcc1, mfcc2):
    distance, _ = fastdtw(mfcc1, mfcc2, radius=5, dist=euclidean)  # fastdtw 取代 dtw
    return distance

# 計算歐式距離
def compute_euclidean(mfcc1_mean, mfcc2_mean):
    return np.linalg.norm(mfcc1_mean - mfcc2_mean)

# 計算余弦相似度
def compute_cosine_similarity(mfcc1_mean, mfcc2_mean):
    # 轉換成 (1, N) 形狀
    mfcc1_mean = mfcc1_mean.reshape(1, -1)
    mfcc2_mean = mfcc2_mean.reshape(1, -1)

    # 確保向量歸一化
    mfcc1_mean = normalize(mfcc1_mean)
    mfcc2_mean = normalize(mfcc2_mean)

    return np.clip(cosine_similarity(mfcc1_mean, mfcc2_mean)[0][0], -1.0, 1.0)

# 比對音頻
def compare_audio(audio_path1, audio_path2):
    print(f"Comparing {audio_path1} and {audio_path2}:")

    # 預計算 MFCC
    mfcc1_mean, mfcc1 = compute_mfcc(audio_path1)
    mfcc2_mean, mfcc2 = compute_mfcc(audio_path2)

    # 1️⃣ MFCC 歐式距離
    euclidean_distance = compute_euclidean(mfcc1_mean, mfcc2_mean)
    euclidean_similarity = max(0, 100 - (euclidean_distance / 100 * 100))  # 假設最大值 100

    # 2️⃣ DTW 距離
    dtw_distance = compute_dtw(mfcc1, mfcc2)
    dtw_similarity = max(0, 100 - (dtw_distance / 500 * 100))  # 假設最大值 500

    # 3️⃣ 余弦相似度
    cosine_sim = compute_cosine_similarity(mfcc1_mean, mfcc2_mean)
    cosine_similarity_percent = (cosine_sim + 1) / 2 * 100

    # 計算平均相似度
    avg_similarity = (euclidean_similarity + dtw_similarity + cosine_similarity_percent) / 3

    print(f"MFCC Euclidean similarity: {euclidean_similarity:.2f}%")
    print(f"DTW similarity: {dtw_similarity:.2f}%")
    print(f"Cosine similarity: {cosine_similarity_percent:.2f}%")
    return f"🔹 **Overall Similarity: {avg_similarity:.2f}%** 🔹"  # 總相似度
