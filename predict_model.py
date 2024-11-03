import pickle
import pandas as pd
import ast

# Load the model from the file
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the dataset
df = pd.read_csv('ml.csv')

# Select the first row of the dataset
first_row = df.iloc[0]

# Define the features
features = ['invasive', 'woody_species_percentage', 'water_sources', 'seed_type', 'years_since_prescribed_burn']

# Extract the feature values for the first row
input_data = first_row[features].values.reshape(1, -1)

# Make a prediction using the model
prediction = model.predict(input_data)

# Output the prediction
print("Predicted result:", "Fall" if prediction[0] == 1 else "Spring")
print("Actual result:", first_row['result'])