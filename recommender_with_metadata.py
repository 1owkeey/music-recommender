import pandas as pd

# Load the track similarity matrix
similarity_df = pd.read_csv('track_similarity_matrix.csv', index_col=0)

# Load the metadata (track names, artist, album, etc.) for the recommendations
tracks_df = pd.read_csv('normalized_track_features.csv')  # Should have track_id, track_name, artist, album, etc.

# Define a function to recommend similar tracks with metadata
def recommend_similar_tracks_with_metadata(track_id, n=5):
    # Check if the track_id exists in the similarity DataFrame
    if track_id not in similarity_df.index:
        print(f"Track ID {track_id} not found in the dataset.")
        return []
    
    # Get the similarity scores for the given track_id
    similarity_scores = similarity_df[track_id]
    
    # Debug: Print the similarity scores for the given track ID
    print(f"Similarity scores for {track_id}:")
    print(similarity_scores)
    
    # Sort the scores in descending order and exclude the track itself (similarity = 1.0)
    similar_tracks = similarity_scores.sort_values(ascending=False).drop(track_id)
    
    # Debug: Print the top n most similar tracks
    print(f"Top {n} similar tracks for {track_id}:")
    print(similar_tracks.head(n))
    
    # Get the top n most similar tracks
    top_n_similar_tracks = similar_tracks.head(n).index.tolist()
    
    # Find the metadata for the similar tracks
    recommendations = tracks_df[tracks_df['track_id'].isin(top_n_similar_tracks)][['track_id', 'track_name', 'artist', 'album']]
    
    return recommendations

# Test the recommender function with a track ID
test_track_id = tracks_df['track_id'].iloc[0]  # Use the first track in the dataset
recommended_tracks = recommend_similar_tracks_with_metadata(test_track_id, n=5)

# Print the recommended tracks with metadata
print(f"Tracks similar to {test_track_id}:")
print(recommended_tracks)