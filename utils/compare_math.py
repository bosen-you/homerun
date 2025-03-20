import librosa  
import numpy as np  
from scipy.spatial.distance import euclidean  
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.preprocessing import normalize 
from fastdtw import fastdtw 
import os 

# Set MFCC parameters
N_MFCC = 25  # You can reduce this to speed up computations
SR = 44100  # Lower sample rate to speed up processing

# Precompute MFCC to avoid redundant calculations
def compute_mfcc(audio_path):
    y, sr = librosa.load(audio_path, sr=SR)  # Load audio with a fixed sample rate
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)  # Extract MFCC features using librosa
    return np.mean(mfcc, axis=1), mfcc.T  # Return the mean and the full MFCC

# Fast DTW (using fastdtw)
def compute_dtw(mfcc1, mfcc2):
    distance, _ = fastdtw(mfcc1, mfcc2, radius=5, dist=euclidean)  # Use fastdtw to calculate DTW distance with Euclidean distance
    return distance

# Calculate Euclidean distance
def compute_euclidean(mfcc1_mean, mfcc2_mean):
    return np.linalg.norm(mfcc1_mean - mfcc2_mean)  # Calculate the Euclidean distance between two vectors

# Calculate cosine similarity
def compute_cosine_similarity(mfcc1_mean, mfcc2_mean):
    # Reshape to (1, N) shape
    mfcc1_mean = mfcc1_mean.reshape(1, -1)
    mfcc2_mean = mfcc2_mean.reshape(1, -1)

    # Normalize vectors
    mfcc1_mean = normalize(mfcc1_mean)  # Normalize the vector using sklearn's normalize function
    mfcc2_mean = normalize(mfcc2_mean)

    return np.clip(cosine_similarity(mfcc1_mean, mfcc2_mean)[0][0], -1.0, 1.0)  # Calculate cosine similarity and ensure result is in range [-1, 1]

# Compare audio
def compare_audio(audio_path1, audio_path2):
    print(f"Comparing {audio_path1} and {audio_path2}:")

    # Precompute MFCC
    mfcc1_mean, mfcc1 = compute_mfcc(audio_path1)
    mfcc2_mean, mfcc2 = compute_mfcc(audio_path2)

    # MFCC Euclidean Distance
    euclidean_distance = compute_euclidean(mfcc1_mean, mfcc2_mean)
    euclidean_similarity = max(0, 100 - (euclidean_distance / 100 * 100))  # Assuming the maximum value is 100

    # DTW Distance
    dtw_distance = compute_dtw(mfcc1, mfcc2)
    dtw_similarity = max(0, 100 - (dtw_distance / 500 * 100))  # Assuming the maximum value is 500

    # Cosine Similarity
    cosine_sim = compute_cosine_similarity(mfcc1_mean, mfcc2_mean)
    cosine_similarity_percent = (cosine_sim + 1) / 2 * 100

    # Calculate average similarity
    avg_similarity = (euclidean_similarity + dtw_similarity + cosine_similarity_percent) / 3

    print(f"MFCC Euclidean similarity: {euclidean_similarity:.2f}%")
    print(f"DTW similarity: {dtw_similarity:.2f}%")
    print(f"Cosine similarity: {cosine_similarity_percent:.2f}%")
    return f"🔹 **Overall Similarity: {avg_similarity:.2f}%** 🔹"  # Overall similarity
