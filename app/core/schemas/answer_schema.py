from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AnswerBase(BaseModel):
    user_id: str
    text: str


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    created_at: datetime
