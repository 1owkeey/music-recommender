import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the extracted audio features
df = pd.read_csv('track_features.csv')

# List of feature columns that need to be normalized
feature_columns = ['tempo', 'spectral_centroid', 'spectral_bandwidth', 
                   'spectral_rolloff', 'zero_crossing_rate', 'chroma_stft']

# Initialize the MinMaxScaler
scaler = MinMaxScaler()

# Fit the scaler to the data and transform the features
df[feature_columns] = scaler.fit_transform(df[feature_columns])

# Display the first few rows of the normalized features
print(df.head())

# Save the normalized features back to a CSV file (optional, but helpful for next steps)
df.to_csv('normalized_track_features.csv', index=False)
print("Normalized features saved to 'normalized_track_features.csv'.")
