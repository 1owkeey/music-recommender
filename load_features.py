import pandas as pd

# Load the extracted audio features from track_features.csv
df = pd.read_csv('track_features.csv')

# Display the first few rows to check the data
print(df.head())
