from enum import Enum
from typing import Dict, Generic, List, Optional, TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field, conlist, constr
from pydantic.generics import GenericModel


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


class ManyAnswer(BaseModel):
    __root__: List[constr(min_length=1)]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class JoinAnswer(BaseModel):
    __root__: Dict[constr(min_length=1), constr(min_length=1)]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


QAType = TypeVar("QAType", str, ManyAnswer, JoinAnswer)


class QA(GenericModel, Generic[QAType]):
    class type_enum(str, Enum):
        one = "Выберите один правильный вариант"
        many = "Выберите все правильные варианты"
        drag = "Перетащите варианты так, чтобы они оказались в правильном порядке"
        join = "Соедините соответствия справа с правильными вариантами"

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda v: str(v)}

    id: StrObjectId = Field(None, alias="_id")
    type: type_enum
    question: constr(min_length=1)
    answers: conlist(constr(min_length=1), min_items=2)
    extra_answers: Optional[conlist(constr(min_length=1), min_items=2)]
    correct: Optional[QAType]
    incorrect: List[QAType] = []
