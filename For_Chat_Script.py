import pickle
import numpy as np

# Load the model from the file
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)
    
def call(invasive, woody_species_percentage, water_sources, seed_type, years_since_prescribed_burn):
	# Function to convert individual inputs to numerical values
	def convert_individual_input(invasive, seed_type):
		invasive_mapping = {'KR': 1, 'JG': 2, 'P': 3}
		water_sources_mapping = {'stream': 1, 'pond': 2, 'well': 3, 'none': 4}
		seed_type_mapping = {'native_grass': 1, 'wildflower': 2}

		invasive_value = sum(invasive_mapping[item] for item in invasive)
		water_sources = water_sources_mapping
		seed_type_value = sum(seed_type_mapping[item] for item in seed_type)

		return invasive_value, seed_type_value

	# Convert individual inputs to numerical values
	invasive_value, seed_type_value = convert_individual_input(invasive, seed_type)

	# Create input array
	input_data = np.array([[invasive_value, woody_species_percentage, water_sources, seed_type_value, years_since_prescribed_burn]])

	# Make a prediction using the model
	prediction = model.predict(input_data)

	# Output the prediction
	return "Fall" if prediction[0] == 1 else "Spring"