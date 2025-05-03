import librosa  
import numpy as np  
from scipy.spatial.distance import euclidean  
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.preprocessing import normalize 
from starlette.responses import JSONResponse
from fastdtw import fastdtw 
import json

# Set MFCC parameters
N_MFCC = 25  # You can reduce this to speed up computations
SR = 44100  # Lower sample rate to speed up processing

# Precompute MFCC to avoid redundant calculations
def compute_mfcc(audio_bytes):
    y, sr = librosa.load(audio_bytes, sr=None, mono=True) 
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  
    return np.mean(mfcc, axis=1), mfcc

# Fast DTW (using fastdtw)
def compute_dtw(mfcc1, mfcc2):
    print(1)
    distance, _ = fastdtw(mfcc1, mfcc2, radius=5, dist=lambda x, y: np.linalg.norm(np.array(x) - np.array(y)))
    print(1)
    return distance

# Calculate Euclidean distance
def compute_euclidean(mfcc1_mean, mfcc2_mean):
    print(1)
    return np.linalg.norm(mfcc1_mean - mfcc2_mean)  # Calculate the Euclidean distance between two vectors

# Calculate cosine similarity
def compute_cosine_similarity(mfcc1_mean, mfcc2_mean):
    print(1)
    # Reshape to (1, N) shape
    mfcc1_mean = mfcc1_mean.flatten().reshape(1, -1)
    mfcc2_mean = mfcc2_mean.flatten().reshape(1, -1)

    # Normalize vectors
    mfcc1_mean = normalize(mfcc1_mean)  # Normalize the vector using sklearn's normalize function
    mfcc2_mean = normalize(mfcc2_mean)

    return np.clip(cosine_similarity(mfcc1_mean, mfcc2_mean)[0][0], -1.0, 1.0)  # Calculate cosine similarity and ensure result is in range [-1, 1]

# Compare audio
def compare_two_audio(audio_bytes1, audio_bytes2):
    # Precompute MFCC
    mfcc1_mean, mfcc1 = compute_mfcc(audio_bytes1)
    mfcc2_mean, mfcc2 = compute_mfcc(audio_bytes2)

    # MFCC Euclidean Distance
    euclidean_distance = compute_euclidean(mfcc1_mean, mfcc2_mean)
    euclidean_similarity = max(0, 100 - (euclidean_distance / 100 * 100))  # Assuming the maximum value is 100

    # DTW Distance
    print(f"mfcc1.mean(axis=1) shape: {mfcc1.mean(axis=1).shape}")
    print(f"mfcc2.mean(axis=1) shape: {mfcc2.mean(axis=1).shape}")
    mfcc1_vec = mfcc1.mean(axis=1).tolist()
    mfcc2_vec = mfcc2.mean(axis=1).tolist()

    dtw_distance = compute_dtw(mfcc1_vec, mfcc2_vec)
    dtw_similarity = max(0, 100 - (dtw_distance / 500 * 100))  # Assuming the maximum value is 500

    # Cosine Similarity
    
    cosine_sim = compute_cosine_similarity(mfcc1_mean, mfcc2_mean)
    cosine_similarity_percent = (cosine_sim + 1) / 2 * 100

    # Calculate average similarity
    avg_similarity = 0.4 * euclidean_similarity + 0.3 * dtw_similarity + 0.3 * cosine_similarity_percent

    return f"MFCC Euclidean similarity: {euclidean_similarity:.2f}%\nDTW similarity: {dtw_similarity:.2f}%\nCosine similarity: {cosine_similarity_percent:.2f}%", float(f"{avg_similarity:.2f}") # Overall similarity