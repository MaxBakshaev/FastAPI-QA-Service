from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .mixin_model import MixinCreatedAt
from .question_model import Question


class Answer(Base, MixinCreatedAt):

    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    question: Mapped["Question"] = relationship(
        back_populates="answers",
        passive_deletes=True,
    )
