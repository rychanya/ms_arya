import pytest

from ms_arya.models import QA


@pytest.fixture
def qa_dict():
    return {"type": QA.type_enum.one, "question": "q", "answers": ["1", "2"]}
