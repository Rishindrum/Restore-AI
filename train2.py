import pandas as pd
import numpy as np

# Load the original dataset
df = pd.read_csv('train.csv')

# Randomly select half of the rows
df_half = df.sample(frac=0.5, random_state=42)

# Save the new dataset to train2.csv
df_half.to_csv('train2.csv', index=False)