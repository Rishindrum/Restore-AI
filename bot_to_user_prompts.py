#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Start of global definitions-------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

import google.generativeai as genai

import json

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
global curr_feature_index

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


#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------End of Database-Management---------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------


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
#----------------------------------------------------------------Feature 1 Prompt------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------


def feature_1_prompt():

    global global_doc_id

    deleteAllDocuments(BotToUser_collectionID)


    feature_1_prompt = f"You are going to serve as a proxy between me and a farmer. This farmer will be giving information about a praire-land restoration project they're working on, and they need to provide some information to me about the properties of their land. You will be asking questions to them on my behalf, and will be interpreting and parsing their responses to store in a database." \
            "The first question you should ask is: what type of invasive species are present on the land. Make sure to mention that the farmer is able to select from one of three options: namely, Johnson Grass, King Ranch, Privet. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."

        
    response = model.generate_content(feature_1_prompt)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

    text_response = trim_quotes(text_response)

    global_doc_id = ID.unique()

    result = db.create_document(databaseId, BotToUser_collectionID, global_doc_id, data ={
        "msg1": text_response
    })

    # global_doc_id = result['$id']

    # print(result)

    # print(text_response)
    # print(f"RTW_Bot: {trim_quotes(text_response)}")

    print(type(global_doc_id))




#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Feature 2 Prompt------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
    
def feature_2_prompt():
    
    feature_2_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The second question you should ask is: approximately what percentage of your plot contains woody species. Make sure to mention that the farmer should provide a number between 0 and 100, representing this percentage. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."


    response = model.generate_content(feature_2_prompt)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

    text_response = trim_quotes(text_response)
    print(text_response)

    result = db.update_document(
        databaseId, 
        BotToUser_collectionID, 
        global_doc_id, 
        data = {
            # "msg1": db.get_document(databaseId, BotToUser_collectionID, global_doc_id)['msg1'],
            "msg2": text_response
            # "msg3": db.get_document(databaseId, BotToUser_collectionID, global_doc_id)['msg3'],
            # "msg4": db.get_document(databaseId, BotToUser_collectionID, global_doc_id)['msg4'],
            # "msg5": db.get_document(databaseId, BotToUser_collectionID, global_doc_id)['msg5'],
            # "msg6": db.get_document(databaseId, BotToUser_collectionID, global_doc_id)['msg6'],
        }
    )



#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Feature 3 Prompt------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
   
def feature_3_prompt():
    feature_3_prompt = f"You are already serving as a proxy between me and a farmer." \
            "Firstly, thank the user for answering the previous question they gave. The third question you should ask is: What bodies of water are nearby your plot of land, if any? Make sure to mention that the farmer should pick between river, spring, lake, and none. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."



    response = model.generate_content(feature_3_prompt)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

    text_response = trim_quotes(text_response)

    db.update_document(databaseId, BotToUser_collectionID, global_doc_id, data ={
        "msg3": text_response
    })



#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Feature 4 Prompt------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
def feature_4_prompt():
    feature_4_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The fourth question you should ask is: What does your seed mix consist of: wildflower or native grass, or both? Make sure to mention that the farmer should pick between the options of wildflower, native grass, or both. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."




    response = model.generate_content(feature_4_prompt)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

    text_response = trim_quotes(text_response)

    db.update_document(databaseId, BotToUser_collectionID, global_doc_id, data ={
        "msg4": text_response
    })



#--------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Feature 5 Prompt------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------
def feature_5_prompt():
    feature_5_prompt = f"You are already serving as a proxy between me and a farmer." \
        "Firstly, thank the user for answering the previous question they gave. The fifth question you should ask is: how many years ago was the last prescribed burn on your plot? Make sure to mention to the user that if they're not sure, then indicate that they weren't sure.  Make sure to mention that the farmer should write a whole number indicating the number of years since the last prescribed burn, or indicate that they weren't sure when the last one was. Write this question as a string on a single line(i.e. don't use bullet points or unnecessary paragraph breaks) in a readable way, prompting the farmer for their response."




    response = model.generate_content(feature_5_prompt)
    text_response = response.text.strip() if hasattr(response, 'text') else response['text'].strip()

    text_response = trim_quotes(text_response)

    db.update_document(databaseId, BotToUser_collectionID, global_doc_id, data ={
        "msg5": text_response
    })


def main(request):

    global curr_feature_index

    payload = json.loads(request.payload)
    curr_feature_index = payload.get("count")




if(__name__ == "__main__"):

    #TODO: Get iteration number
    iteration_num = curr_feature_index

    if(iteration_num == 1):
        feature_1_prompt()
    elif(iteration_num == 2):
        feature_2_prompt()
    elif(iteration_num == 3):
        feature_3_prompt()
    elif(iteration_num == 4):
        feature_4_prompt()
    elif(iteration_num == 5):
        feature_5_prompt()

    # feature_1_prompt()
    # feature_2_prompt()
    # feature_3_prompt()
    # feature_4_prompt()
    # feature_5_prompt()

        