from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the track similarity matrix and metadata (from previous steps)
similarity_df = pd.read_csv('track_similarity_matrix.csv', index_col=0)
tracks_df = pd.read_csv('normalized_track_features.csv')  # Contains track metadata like track_name, artist, album

# Convert all track IDs to lowercase for case-insensitive matching
similarity_df.index = similarity_df.index.str.lower()
tracks_df['track_id'] = tracks_df['track_id'].str.lower()

# Recommender function
def recommend_similar_tracks_with_metadata(track_id, n=5):
    if track_id not in similarity_df.index:
        return pd.DataFrame()  # Return empty DataFrame if track not found
    
    # Get similarity scores
    similarity_scores = similarity_df[track_id].sort_values(ascending=False).drop(track_id)
    
    # Get top n similar tracks
    top_n_similar_tracks = similarity_scores.head(n).index.tolist()
    
    # Get metadata for the recommended tracks
    recommendations = tracks_df[tracks_df['track_id'].isin(top_n_similar_tracks)][['track_id', 'track_name', 'artist', 'album']]
    
    return recommendations

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Route to handle recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    track_id = request.form['track_id'].strip().lower()  # Get the track ID from the form and convert to lowercase
    
    # Handle empty input
    if not track_id:
        return render_template('recommend.html', error="Please provide a valid Track ID.")
    
    # Generate recommendations
    recommendations = recommend_similar_tracks_with_metadata(track_id)
    
    # If no recommendations found, show error
    if recommendations.empty:
        return render_template('recommend.html', track_id=track_id, error="Track not found.")
    
    # Display the recommendations
    return render_template('recommend.html', track_id=track_id, recommendations=recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)