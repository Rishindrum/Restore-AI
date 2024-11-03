#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Start of global definitions-------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

import google.generativeai as genai

# TOOD: Make sure 
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def trim_quotes(s):
    # Strip whitespace, then check first/last non-blank characters
    s_stripped = s.strip()
    if s_stripped and s_stripped[0] == '"':
        s_stripped = s_stripped[1:]
    if s_stripped and s_stripped[-1] == '"':
        s_stripped = s_stripped[:-1]
    
    # Preserve original spacing by replacing middle part
    start_spaces = len(s) - len(s.lstrip())
    end_spaces = len(s) - len(s.rstrip())
    return ' ' * start_spaces + s_stripped + ' ' * end_spaces


global_doc_id = ""
global global_user_response_doc


#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------End of global definitions---------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------










#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Database-Management---------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------


from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from appwrite.id import ID


# Initialize Appwrite Client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Your API Endpoint
client.set_project('67267a89001c3c867be1')  # Your project ID
client.set_key('standard_a1ca356c8c0f40de30d5e2358473ca1ae1de3a6d347d7a3294abcd2a264c80cc1ac185c3a6eac5c9c0240e357aaa4892457760e7e254047f40589293feb08052aa2141a6f683af348814bb99043e7779f5158c51fead62695c03a15127106d7d471bea8d0dec5bf49587f989e6ca9b2c953ae6d21a5c46249362fc65f2a618ad')  # Your API key
 
# Initialize Databases service
db = Databases(client)

projectId = '67267a89001c3c867be1'
databaseId = '67267ef2000ed7e975ea'

messages_collectionID = '6726eb330017830de795'
features_collectionID = '67267efe000276d5ca45'
UserToBot_collectionID = '6726f71b0011cef89640'
BotToUser_collectionID = '6726f6c8001cd4de9a00'



#Delete all documents
def deleteAllDocuments(collection):
    try:
        # List all documents in the collection
        response = db.list_documents(databaseId, collection, [Query.limit(500)])
        documents = response['documents']

        for document in documents:
            document_id = document['$id']
            try:
                db.delete_document(databaseId, collection, document_id)
            except Exception as e:
                print(f"Error deleting document {document_id}: {e}")

    except Exception as e:
        print(f"Error fetching documents: {e}")


#Switch Statement Here TODO





#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------End of Database-Management---------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------






def get_doc():
    global global_user_response_doc

    global_user_response_doc = db.list_documents(databaseId, UserToBot_collectionID, [Query.limit(1)])['documents'][0]

    # print(global_user_response_doc)



def feature_1_database_store():

    global global_doc_id

    deleteAllDocuments(features_collectionID)

    # print(global_user_response_doc)

    feature_1_user_response = global_user_response_doc['msg1']
    # feature_1_user_response = "User: My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it.\n\n"
    # print(feature_1_user_response)

    feature_1_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what types of invasive species are present on their land, and they had to pick between Johnson Grass, King Ranch, Privet. The following was their response: {feature_1_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which invasive species is present on their land, such that this string will end up in a database. If their answer didn't clearly state one of the 3 options, please return an empty string."

    response = model.generate_content(feature_1_database_store)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()
    text_response = trim_quotes(text_response)

    array = [item.strip() for item in text_response.split(',')]
    result_array = []

    for i in range(len(array)):
        if "Johnson Grass" in array[i]:
            result_array.append("JG")
        if "King Ranch" in array[i]:
            result_array.append("KR")
        if "Privet" in array[i]:
            result_array.append("P")


    global_doc_id = ID.unique()

    db.create_document(databaseId, features_collectionID, global_doc_id, data ={
        "invasive": result_array
    })



def feature_2_database_store():

    # print(global_user_response_doc)

    feature_2_user_response = global_user_response_doc['msg2']
    # feature_1_user_response = "User: My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it.\n\n"
    # print(feature_1_user_response)

    feature_2_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about approximately what percentage of their plot contains woody species, and they responded with a percentage between 0 and 100. The following was their response: {feature_2_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single floating point number that indicates the percentage the farmer indicated, such that this floating point will end up in a database. If their answer didn't clearly give a response, please return an empty output."


    response = model.generate_content(feature_2_database_store)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()
    text_response = trim_quotes(text_response)


    db.update_document(databaseId, features_collectionID, global_doc_id, data ={
        "woody_species_percentage": float(text_response)
    })



def feature_3_database_store():


    # print(global_user_response_doc)

    feature_3_user_response = global_user_response_doc['msg3']
    # feature_1_user_response = "User: My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it.\n\n"
    # print(feature_1_user_response)

    feature_3_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what bodies of water are nearby their plot of land, if any. The following was their response: {feature_3_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which types of bodies of water are near their land, such that this string will end up in a database. If their answer didn't clearly state one of the 4 options, please return an empty string."


    response = model.generate_content(feature_3_database_store)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()
    text_response = trim_quotes(text_response)

    # print(text_response)


    db.update_document(databaseId, features_collectionID, global_doc_id, data ={
        "water_sources": text_response.lower()
    })


def feature_4_database_store():


    # print(global_user_response_doc)

    feature_4_user_response = global_user_response_doc['msg4']
    # feature_1_user_response = "User: My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it.\n\n"
    # print(feature_1_user_response)

    feature_4_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about what does their seed mix consist of: wildflower or native grass, or both. The following was their response: {feature_4_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single string that indicates which type of seed mix they used, choosing between wildflower, native grass, or both, such that this string will end up in a database. If their answer didn't clearly state one of the 3 options, please return an empty string."
        


    response = model.generate_content(feature_4_database_store)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()
    text_response = trim_quotes(text_response)

    array = [item.strip() for item in text_response.lower().split(',')]
    result_array = []

    for i in range(len(array)):
        if "wildflower" in array[i]:
            result_array.append("wildflower")
        if "native grass" in array[i]:
            result_array.append("native_grass")
        if "both" in array[i]:
            result_array.append("native_grass")
            result_array.append("wildflower")
            


    db.update_document(databaseId, features_collectionID, global_doc_id, data ={
        "seed_type": result_array
    })

def feature_5_database_store():


    # print(global_user_response_doc)

    feature_5_user_response = global_user_response_doc['msg5']
    # feature_1_user_response = "User: My plot has a ton of Johnson Grass and Privet, but I've been working to get rid of it.\n\n"
    # print(feature_1_user_response)

    feature_5_database_store = f"You are already serving as a proxy between me and a farmer. You just asked a question to them about how many years ago was the last prescribed burn on their plot. The following was their response: {feature_5_user_response}. Given this response, I need you to parse the farmer's response and provide to me a single integer that indicates how long ago the most recent prescribed burn, such that this integer will end up in a database. If they said that they weren't sure how long ago the last prescribed burn was, please return the integer 20."



    response = model.generate_content(feature_5_database_store)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()
    text_response = trim_quotes(text_response)



    db.update_document(databaseId, features_collectionID, global_doc_id, data ={
        "years_since_prescribed_burn": float(text_response)
    })
    


    

     


if(__name__ == "__main__"):
    get_doc()
    feature_1_database_store()
    feature_2_database_store()
    feature_3_database_store()
    feature_4_database_store()
    feature_5_database_store()