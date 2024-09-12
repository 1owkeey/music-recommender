import pandas as pd
import os

# Load the raw data (make sure 'saved_tracks.csv' exists and is correctly populated)
if os.path.exists('saved_tracks.csv'):
    df = pd.read_csv('saved_tracks.csv')

    # Perform any necessary data cleaning or transformations
    # Example: dropping missing values
    df.dropna(inplace=True)

    # Save the cleaned data
    df.to_csv('cleaned_tracks.csv', index=False)
    print("Cleaned data saved to 'cleaned_tracks.csv'.")
else:
    print("Error: 'saved_tracks.csv' not found. Please ensure the data collection process is complete.")
