from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from . import AnswerRead


class QuestionBase(BaseModel):
    text: str = Field(min_length=1)


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    answers: List["AnswerRead"] = []
