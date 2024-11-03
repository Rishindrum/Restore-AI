
import csv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query


# Initialize Appwrite Client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Your API Endpoint
client.set_project('67267a89001c3c867be1')  # Your project ID
client.set_key('standard_a1ca356c8c0f40de30d5e2358473ca1ae1de3a6d347d7a3294abcd2a264c80cc1ac185c3a6eac5c9c0240e357aaa4892457760e7e254047f40589293feb08052aa2141a6f683af348814bb99043e7779f5158c51fead62695c03a15127106d7d471bea8d0dec5bf49587f989e6ca9b2c953ae6d21a5c46249362fc65f2a618ad')  # Your API key
 
# Initialize Databases service
databases = Databases(client)

# Define your database and collection IDs
database_id = '67267ef2000ed7e975ea'
collection_id = '67267efe000276d5ca45'

# Function to fetch all documents from the collection
def fetch_all_documents(database_id, collection_id):
    documents = []
    limit = 500  # Fetch 100 documents per request (maximum allowed by Appwrite)
    offset = 0   # Start at offset 0

    while True:
        # Fetch documents with pagination
        result = databases.list_documents(database_id, 
                                          collection_id, [Query.limit(500)]
                                          )
        documents.extend(result['documents'])

        # Break if we have fetched all documents
        if len(result['documents']) < limit:
            break

        # Increase the offset to fetch the next batch
        offset += limit

    return documents

# Function to save documents to CSV
def save_to_csv(documents, file_name):
    # Ensure there's at least one document to get the keys
    if not documents:
        print("No documents found.")
        return

    # Extract field names from the first document
    fieldnames = documents[0].keys()

    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write header row
        writer.writerows(documents)  # Write document data

    print(f"Data has been saved to {file_name}")

# Fetch all documents from the specified collection
documents = fetch_all_documents(database_id, collection_id)

# Save documents to a CSV file
save_to_csv(documents, 'appwrite_collection_final.csv')














