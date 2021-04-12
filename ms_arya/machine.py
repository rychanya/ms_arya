from ms_arya.combinations import get_answer
from ms_arya.db import add_correct_answer, add_incorrect_answer, find_or_create
from ms_arya.models import QA


class QAMachine:
    def __init__(self, **data):
        qa = QA.parse_obj(data)
        self.qa: QA = find_or_create(qa)
        assert self.qa is not None
        self._answer = None
        self._is_correct = None

    @property
    def answer(self):
        if self._answer is None:
            self._answer = get_answer(self.qa)
        return self._answer

    @property
    def is_correct(self):
        return self._is_correct

    @is_correct.setter
    def is_correct(self, value):
        if value:
            add_correct_answer(self.qa, self.answer)
        else:
            add_incorrect_answer(self.qa, self.answer)
        self._is_correct = bool(value)
