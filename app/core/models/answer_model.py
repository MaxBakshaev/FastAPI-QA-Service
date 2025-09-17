from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base, MixinCreatedAt

if TYPE_CHECKING:
    from . import Question


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
        "Question",
        back_populates="answers",
        passive_deletes=True,
    )
