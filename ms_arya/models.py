from enum import Enum
from typing import List, Union

from bson import ObjectId
from pydantic import BaseModel, Field, conlist, constr


class StrObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError(f"{v} is not valid ObjectId")
            return ObjectId(v)
        elif isinstance(v, ObjectId):
            if not ObjectId.is_valid(str(v)):
                ValueError(f"{v} is not valid ObjectId")
            return v
        else:
            raise TypeError("str or ObjectId required")


class type_enum(str, Enum):
    one = "Выберите один правильный вариант"
    many = "Выберите все правильные варианты"
    drag = "Перетащите варианты так, чтобы они оказались в правильном порядке"
    join = "Соедините соответствия справа с правильными вариантами"


not_empty_str = constr(min_length=1)
list_with_min_two_items = conlist(not_empty_str, min_items=2)


class QA(BaseModel):
    id: StrObjectId = Field(None, alias="_id")
    type: type_enum
    question: not_empty_str
    answers: list_with_min_two_items
    correct: Union[None, not_empty_str, list_with_min_two_items]
    incorrect: List[Union[not_empty_str, list_with_min_two_items]] = []

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda v: str(v)}
