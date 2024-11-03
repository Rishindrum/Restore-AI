import pandas as pd
import numpy as np

# Load the original dataset
df = pd.read_csv('appwrite_collection_final.csv')

# Transform the 'invasive' column into a binary column
for i in range(len(df)):
	count = 0
	# In each row, if there is an instance of 'KR', add 1 to the count
	if 'KR' in df['invasive'][i]:
		count += 1
	if 'JG' in df['invasive'][i]:
		count += 2
	if 'P' in df['invasive'][i]:
		count += 3
	df.loc[i, 'invasive'] = count
	count = 0
	if 'river' in df['water_sources'][i]:
		count += 1
	if 'spring' in df['water_sources'][i]:
		count += 2
	if 'lake' in df['water_sources'][i]:
		count += 3
	if 'none' in df['water_sources'][i]:
		count += 4
	df.loc[i, 'water_sources'] = count
	count = 0
	if 'native_grass' in df['seed_type'][i]:
		count += 1
	if 'wildflower' in df['seed_type'][i]:
		count += 2
	df.loc[i, 'seed_type'] = count

# Save the new dataset to train2.csv
df.to_csv('ml.csv', index=False)