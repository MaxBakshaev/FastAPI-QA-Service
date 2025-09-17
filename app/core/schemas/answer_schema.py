from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class AnswerBase(BaseModel):
    text: str = Field(min_length=1)


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    user_id: str
    created_at: datetime
