import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read"
))

# Fetch user's saved tracks and include preview URLs
def fetch_user_saved_tracks():
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    track_list = []

    for item in tracks:
        track = item['track']
        track_info = {
            'track_name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'track_id': track['id'],
            'preview_url': track['preview_url']  # Include the preview URL
        }
        track_list.append(track_info)

    return pd.DataFrame(track_list)

# Save the data to a CSV file
if __name__ == "__main__":
    df = fetch_user_saved_tracks()
    df.to_csv('saved_tracks_with_previews.csv', index=False)
    print("Data with preview URLs saved to 'saved_tracks_with_previews.csv'")

