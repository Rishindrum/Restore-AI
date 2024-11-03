import pickle
import numpy as np
import pandas as pd

# Load the model from the file
with open('try_again.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the dataset
df = pd.read_csv('ml.csv')

# Select the first row of the dataset
first_row = df.iloc[0]

# Define the features
features = ['invasive', 'woody_species_percentage', 'water_sources', 'seed_type', 'years_since_prescribed_burn']

# Extract the feature values for the first row
input_data = first_row[features].values.reshape(1, -1)

# Make a prediction with a decision tree
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']

# Make a prediction with a list of bagged trees
def bagging_predict(trees, row):
	predictions = [predict(tree, row) for tree in trees]
	return max(set(predictions), key=predictions.count)

# Make a prediction using the model
prediction = bagging_predict(model, input_data[0])

# Output the prediction
print(prediction)
print("Predicted result:", "Fall" if prediction == 1 else "Spring")
print("Actual result:", first_row['result'])