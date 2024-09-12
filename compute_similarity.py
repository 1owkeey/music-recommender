import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the normalized audio features
df = pd.read_csv('normalized_track_features.csv')

# Select the feature columns to compute similarity on
feature_columns = ['tempo', 'spectral_centroid', 'spectral_bandwidth', 
                   'spectral_rolloff', 'zero_crossing_rate', 'chroma_stft']

# Compute the cosine similarity matrix
similarity_matrix = cosine_similarity(df[feature_columns])

# Convert the similarity matrix to a DataFrame for easier access
# The matrix will have track IDs as both rows and columns
similarity_df = pd.DataFrame(similarity_matrix, index=df['track_id'], columns=df['track_id'])

# Display the first few rows of the similarity matrix
print(similarity_df.head())

# Save the similarity matrix to a CSV file (optional)
similarity_df.to_csv('track_similarity_matrix.csv', index=True)
print("Track similarity matrix saved to 'track_similarity_matrix.csv'.")
