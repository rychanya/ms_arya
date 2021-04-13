from ms_arya.combinations import get_answer
from ms_arya.db import add_correct_answer, add_incorrect_answer, find_or_create
from ms_arya.models import QA


class QAMachine:
    def __init__(self, **data):
        qa = QA.parse_obj(data)
        self.qa: QA = find_or_create(qa)
        assert self.qa is not None
        self._answer = None

    @property
    def answer(self):
        if self._answer is None:
            self._answer = get_answer(self.qa)
        return self._answer

    def save_answer(self, is_correct: bool):
        if is_correct:
            add_correct_answer(self.qa, self.answer)
        else:
            add_incorrect_answer(self.qa, self.answer)
