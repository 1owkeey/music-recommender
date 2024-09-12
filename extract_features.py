import librosa
import pandas as pd
import os

# Load the cleaned data
df = pd.read_csv('cleaned_tracks.csv')

# Filter out tracks that are missing their corresponding audio files
df = df[df['track_id'].apply(lambda x: os.path.exists(f"audio_files/{x}.mp3"))]

# Function to extract audio features from a track
def extract_audio_features(audio_file_path):
    y, sr = librosa.load(audio_file_path, duration=30)  # Load the first 30 seconds of the track
    
    # Ensure the correct usage of librosa functions
    tempo = librosa.beat.tempo(y=y, sr=sr)[0]
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y).mean()
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr).mean()
    
    # Pack all features into a dictionary
    features = {
        'tempo': tempo,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'spectral_rolloff': spectral_rolloff,
        'zero_crossing_rate': zero_crossing_rate,
        'chroma_stft': chroma_stft
    }
    return features

# Extract features for each track that has an audio file
feature_list = []
for index, row in df.iterrows():
    audio_path = f"audio_files/{row['track_id']}.mp3"
    try:
        features = extract_audio_features(audio_path)
        feature_list.append({**row, **features})
    except Exception as e:
        print(f"Error processing track {row['track_id']}: {e}")

# Convert the list of features to a DataFrame and save it
if feature_list:
    features_df = pd.DataFrame(feature_list)
    features_df.to_csv('track_features.csv', index=False)
    print("Audio features saved to 'track_features.csv'")
else:
    print("No features were extracted. Please check your audio files and script.")
