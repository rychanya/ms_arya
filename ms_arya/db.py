from os import getenv
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

load_dotenv()

URI = getenv("ARYA_URI", None)
DB_NAME = getenv("ARYA_DB_NAME", "TEST_DB")
COLLECTION_NAME = getenv("ARYA_COLLECTION_NAME", "TEST_COLLECTION")


def get_collection() -> Optional[Collection]:
    try:
        db = client.get_database(DB_NAME)
        collection = db.get_collection(COLLECTION_NAME)
        return collection
    except ConnectionFailure:
        return None


client = MongoClient(URI)
