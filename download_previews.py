import pandas as pd
import requests
import os

# Load the data with preview URLs
df = pd.read_csv('saved_tracks_with_previews.csv')

# Ensure the audio_files directory exists
if not os.path.exists('audio_files'):
    os.makedirs('audio_files')

# Function to download an audio file
def download_audio(preview_url, track_id):
    response = requests.get(preview_url)
    if response.status_code == 200:
        with open(f'audio_files/{track_id}.mp3', 'wb') as file:
            file.write(response.content)
            print(f"Downloaded {track_id}.mp3")
    else:
        print(f"Failed to download {track_id}.mp3")

# Download all available preview URLs
for index, row in df.iterrows():
    if pd.notna(row['preview_url']):  # Check if preview_url is not NaN
        download_audio(row['preview_url'], row['track_id'])
    else:
        print(f"No preview available for {row['track_name']} by {row['artist']}")

print("Download completed.")
