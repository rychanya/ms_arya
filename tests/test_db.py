import pytest
from bson.objectid import ObjectId
from pytest_mock import MockerFixture

from ms_arya.db import find_or_create, get_collection
from ms_arya.models import QA


@pytest.fixture()
def fake_db(mocker: MockerFixture):
    mocker.patch("ms_arya.db.config.DB_COLLECTION_NAME", "TEST_COL")
    collection = get_collection()
    if collection.name == "TEST_COL":
        collection.drop()
    yield
    if collection.name == "TEST_COL":
        collection.drop()


def test_find_or_create(fake_db, qa_dict):
    qa = QA.parse_obj(qa_dict)
    # create
    result1 = find_or_create(qa)
    assert isinstance(result1.id, ObjectId)
    assert get_collection().count_documents({}) == 1
    # find
    result2 = find_or_create(qa)
    assert get_collection().count_documents({}) == 1
    assert result1.id == result2.id
    # find reverse answers
    qa_dict["answers"].reverse()
    qa = QA.parse_obj(qa_dict)
    result3 = find_or_create(qa)
    assert get_collection().count_documents({}) == 1
    assert result1.id == result3.id
