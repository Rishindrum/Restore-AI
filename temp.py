# From ml.csv, get all the unique values in the 'water_sources' column and print them.

import pandas as pd

# Load the original dataset
df = pd.read_csv('appwrite_collection_final.csv')

print(df['water_sources'].unique())