from itertools import chain, combinations, permutations, product
from random import choice

from ms_arya.models import QA


def _one(qa: QA):
    if qa.incorrect:
        answers = set(qa.answers).difference(qa.incorrect)
        if answers:
            return list(answers)
    return qa.answers


def _many(qa: QA):
    all_answers = list(
        chain(*[combinations(qa.answers, n) for n in range(1, len(qa.answers) + 1)])
    )
    if qa.incorrect:
        incorrect = list(map(set, qa.incorrect))
        answers = list(filter(lambda answer: set(answer) not in incorrect, all_answers))
        if answers:
            return answers
    return all_answers


def _drag(qa: QA):
    all_answers = list(permutations(qa.answers, len(qa.answers)))
    if qa.incorrect:
        answers = list(filter(lambda answer: answer not in qa.incorrect, all_answers))
        if answers:
            return answers
    return all_answers


def _join(qa: QA):
    all_answers = []
    for answer in map(
        lambda v: dict(zip(*v)),
        product(permutations(qa.answers), permutations(qa.extra_answers)),
    ):
        if answer not in all_answers:
            all_answers.append(answer)
    if qa.incorrect:
        answers = list(filter(lambda answer: answer not in qa.incorrect, all_answers))
        if answers:
            return answers
    return all_answers


func_dict = {
    QA.type_enum.one: _one,
    QA.type_enum.many: _many,
    QA.type_enum.drag: _drag,
    QA.type_enum.join: _join,
}


def get_answer(qa: QA):
    if qa.correct:
        return qa.correct
    return choice(func_dict[qa.type])
