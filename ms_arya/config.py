from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_URI = getenv("ARYA_DB_URI", None)
DB_NAME = getenv("ARYA_DB_NAME", "TEST_DB")
DB_COLLECTION_NAME = getenv("ARYA_DB_COLLECTION_NAME", "TEST_COLLECTION")
