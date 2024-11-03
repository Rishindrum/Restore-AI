from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import random

# Initialize Appwrite Client
client = Client()

client.set_endpoint('https://cloud.appwrite.io/v1')  # Your API Endpoint
client.set_project('67267a89001c3c867be1')  # Your project ID
client.set_key('standard_a1ca356c8c0f40de30d5e2358473ca1ae1de3a6d347d7a3294abcd2a264c80cc1ac185c3a6eac5c9c0240e357aaa4892457760e7e254047f40589293feb08052aa2141a6f683af348814bb99043e7779f5158c51fead62695c03a15127106d7d471bea8d0dec5bf49587f989e6ca9b2c953ae6d21a5c46249362fc65f2a618ad')  # Your API key


# Initialize Databases service
databases = Databases(client)

# Your database ID and collection ID
database_id = '67268b4b002c2e71d6b8'
collection_id = '67268b53002f7729d865'
# Constants with correct case and format
INVASIVE_OPTIONS = [
    ["KR", "JG"],
    ["KR", "P"],
    ["JG", "P"],
    ["KR"],
    ["P"],
    ["JG"]
]

WATER_SOURCES = ["lake", "spring", "river nearby", "none"]

SEED_TYPES = [
    ["native_grass", "wildflower"],
    ["wildflower", "native_grass"],
    ["native_grass"],
    ["wildflower"]
]


def create_entries(database_id, collection_id):
    for _ in range(50):
        try:
            result = databases.create_document(
                database_id=database_id,
                collection_id=collection_id,
                document_id=ID.unique(),
                data={
                    "invasive": random.choice(INVASIVE_OPTIONS),
                    "woody_species_percentage": round(random.uniform(5, 50), 1),
                    "water_sources": random.choice(WATER_SOURCES),
                    "seed_type": random.choice(SEED_TYPES),
                    "years_since_prescribed_burn": random.randint(0, 25)
                }
            )
            print(f"Created entry with ID: {result}")
        except Exception as e:
            print(f"Error creating entry: {e}")

    
# Usage
DATABASE_ID = '67267ef2000ed7e975ea'     # Replace with your database ID
COLLECTION_ID = '67267efe000276d5ca45' # Replace with your collection ID

create_entries(DATABASE_ID, COLLECTION_ID)







