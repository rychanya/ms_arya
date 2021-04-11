from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection, ReturnDocument

from ms_arya import config
from ms_arya.models import QA

client = MongoClient(config.DB_URI)


def get_collection() -> Optional[Collection]:
    db = client.get_database(config.DB_NAME)
    collection = db.get_collection(config.DB_COLLECTION_NAME)
    return collection


def find_or_create(qa: QA) -> QA:
    filter = {
        "question": qa.question,
        "type": qa.type,
        "answers": {"$all": [{"$elemMatch": {"$eq": answer}} for answer in qa.answers]},
    }
    update = {"$setOnInsert": {"answers": qa.answers}}
    if qa.type == QA.type_enum.join:
        filter.update(
            {
                "extra_answers": {
                    "$all": [
                        {"$elemMatch": {"$eq": answer}} for answer in qa.extra_answers
                    ]
                }
            }
        )
        update["$setOnInsert"].update({"extra_answers": qa.extra_answers})
    data = get_collection().find_one_and_update(
        filter=filter, update=update, upsert=True, return_document=ReturnDocument.AFTER
    )
    return QA.parse_obj(data)


def add_correct_answer(qa: QA, answer):
    filter = qa.dict(include={"id"}, by_alias=True)
    update = {"$set": {"correct": answer}}
    get_collection().find_one_and_update(filter=filter, update=update)


def add_incorrect_answer(qa: QA, answer):
    filter = qa.dict(include={"id"}, by_alias=True)
    update = {"$addToSet": {"incorrect": answer}}
    get_collection().find_one_and_update(filter=filter, update=update)
