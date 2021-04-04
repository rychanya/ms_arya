import pytest
from pydantic import ValidationError

from ms_arya.models import QA


@pytest.fixture
def qa_dict():
    return {"type": QA.type_enum.one, "question": "q", "answers": ["1", "2"]}


@pytest.mark.parametrize("value", ["", None])
def test_empty_question(qa_dict: dict, value):
    qa_dict["question"] = value
    with pytest.raises(ValidationError):
        QA.parse_obj(qa_dict)


@pytest.mark.parametrize("value", [[], ["1"], ["", 1], ["", "", ""]])
def test_empty_or_short_answers(qa_dict: dict, value):
    qa_dict["answers"] = value
    with pytest.raises(ValidationError):
        QA.parse_obj(qa_dict)


def test_incorect_type(qa_dict):
    qa_dict["type"] = "not in type enum"
    with pytest.raises(ValidationError):
        QA.parse_obj(qa_dict)


def test_normal_parse_obj(qa_dict):
    qa = QA.parse_obj(qa_dict)
    assert qa.question == qa_dict["question"]
    assert list(qa.answers) == qa_dict["answers"]
    assert qa.incorrect == []
    assert qa.id is None
    assert qa.correct is None


@pytest.mark.parametrize("id", ["", "604b90df54eb0375d5e96fake"])
def test_incorect_id(qa_dict, id):
    qa_dict["id"] = id
    with pytest.raises(ValidationError):
        QA.parse_obj(qa_dict)
