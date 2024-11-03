from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query


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

if(__name__ == "__main__"):
    deleteAllDocuments(UserToBot_collectionID)