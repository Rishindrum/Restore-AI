import pickle
import numpy as np
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query

global global_user_response_doc

# Initialize Appwrite Client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Your API Endpoint
client.set_project('67267a89001c3c867be1')  # Your project ID
client.set_key('standard_a1ca356c8c0f40de30d5e2358473ca1ae1de3a6d347d7a3294abcd2a264c80cc1ac185c3a6eac5c9c0240e357aaa4892457760e7e254047f40589293feb08052aa2141a6f683af348814bb99043e7779f5158c51fead62695c03a15127106d7d471bea8d0dec5bf49587f989e6ca9b2c953ae6d21a5c46249362fc65f2a618ad')  # Your API key
 
# Initialize Databases service
db = Databases(client)

# Define your database and collection IDs

endpoint = 'https://cloud.appwrite.io/v1'
projectId = '67267a89001c3c867be1'
databaseId = '67267ef2000ed7e975ea'

messages_collectionID = '6726eb330017830de795'
features_collectionID = '67267efe000276d5ca45'
UserToBot_collectionID = '6726f71b0011cef89640'
BotToUser_collectionID = '6726f6c8001cd4de9a00'

# Function to convert individual inputs to numerical values
def convert_individual_input(invasive, water_sources, seed_type):
	invasive_mapping = {'KR': 3, 'JG': 5, 'P': 7}
	water_sources_mapping = {'river': 1, 'spring': 2, 'lake': 3, 'none': 4}
	seed_type_mapping = {'native_grass': 1, 'wildflower': 2}
	
	invasive_value = sum(invasive_mapping[item] for item in invasive)
	water_sources_value = water_sources_mapping[water_sources]
	seed_type_value = sum(seed_type_mapping[item] for item in seed_type)
	
	return invasive_value, water_sources_value, seed_type_value

def predict_individual(invasive, woody_species_percentage, water_sources, seed_type, years_since_prescribed_burn):
	# Load the model from the file
	with open('random_forest_model.pkl', 'rb') as file:
		model = pickle.load(file)
	
	# Convert individual inputs to numerical values
	invasive_value, water_sources_value, seed_type_value = convert_individual_input(invasive, water_sources, seed_type)

	# Create input array
	input_data = np.array([[invasive_value, woody_species_percentage, water_sources_value, seed_type_value, years_since_prescribed_burn]])

	# Make a prediction using the model
	prediction = model.predict(input_data)

	# Output the prediction
	# print("Predicted result:", "Fall" if prediction[0] == 1 else "Spring")

	return "Fall" if prediction[0] == 1 else "Spring"


def get_doc():
	global global_user_response_doc
	global_user_response_doc = db.list_documents(databaseId, features_collectionID, [Query.limit(1)])['documents'][0]


def pushResult(rez):
    db.update_document(
        databaseId, features_collectionID, global_user_response_doc['$id'], data = {
            "result": rez
        }
    )

if __name__ == '__main__':
	get_doc()
	# print(global_user_response_doc)

	# Inputting into the model
	invasive = global_user_response_doc['invasive']
	woody_species_percentage = global_user_response_doc['woody_species_percentage']
	water_sources = global_user_response_doc['water_sources']
	seed_type = global_user_response_doc['seed_type']
	years_since_prescribed_burn = global_user_response_doc['years_since_prescribed_burn']
	prediction = predict_individual(invasive, woody_species_percentage, water_sources, seed_type, years_since_prescribed_burn)
	# print(prediction)

	# Update the document with the prediction
	pushResult(prediction)