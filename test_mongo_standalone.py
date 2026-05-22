from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)

uri = os.getenv("MENTRA_MONGO_URI")
db_name = os.getenv("MENTRA_MONGO_DB")

print(f"Connecting to: {uri}")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    info = client.server_info()
    print("✅ Connection Successful!")
    print(f"Info: {info.get('version')}")
    
    db = client[db_name]
    collections = db.list_collection_names()
    print(f"Collections: {collections}")
    
    # Test insert
    test_coll = db["test_collection"]
    res = test_coll.insert_one({"test": "manual_check"})
    print(f"✅ Insert Successful: {res.inserted_id}")

except Exception as e:
    print(f"❌ Connection Failed: {e}")
