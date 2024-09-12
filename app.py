from flask import Flask, render_template, request
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Load the similarity matrix and metadata
similarity_df = pd.read_csv('track_similarity_matrix.csv', index_col=0)
tracks_df = pd.read_csv('normalized_track_features.csv')  # Should contain track_id, track_name, artist, album

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

# Route for the home page (input form)
@app.route('/')
def home():
    return render_template('home.html')

# Route for recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    track_id = request.form['track_id']  # Get the track ID from the form input
    recommendations = recommend_similar_tracks_with_metadata(track_id)
    
    if recommendations.empty:
        return render_template('recommend.html', track_id=track_id, error="Track not found.")
    
    # Pass the recommendations to the template
    return render_template('recommend.html', track_id=track_id, recommendations=recommendations)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
