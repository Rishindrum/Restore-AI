import pandas as pd
import numpy as np
import pickle
import ast
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('ml.csv')

# Define the features and target variable
features = ['invasive', 'woody_species_percentage', 'water_sources', 'seed_type', 'years_since_prescribed_burn']
target = 'result'

# Convert target variable to numerical
df[target] = df[target].map({'Fall': 1, 'Spring': 0})

# Split the data into training and testing sets
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Save the model to a file
with open('random_forest_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained and saved successfully.")