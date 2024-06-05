from pymongo import MongoClient

def migrate_all_collections(source_uri, destination_uri, db_name):
    # Connect to the source MongoDB database
    source_client = MongoClient(source_uri)
    source_db = source_client[db_name]

    # Connect to the destination MongoDB database
    destination_client = MongoClient(destination_uri)
    destination_db = destination_client[db_name]

    # Iterate over all collections in the source database
    for collection_name in source_db.list_collection_names():
        source_collection = source_db[collection_name]
        destination_collection = destination_db[collection_name]

        # Fetch data from the source collection
        documents = list(source_collection.find())

        # Insert data into the destination collection
        if destination_collection.count_documents({}) > 0:
            print(f"Destination collection '{collection_name}' is not empty!")
        else:
            destination_collection.insert_many(documents)  # Use insert_many to bulk insert documents
            print(f"Data migration for collection '{collection_name}' completed successfully.")


# Example Configuration
source_uri = 'mongodb://source-host:27017'
destination_uri = 'mongodb://destination-host:27017'
db_name = 'your_db_name'

migrate_all_collections(source_uri, destination_uri, db_name)
