from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .mixin_model import MixinCreatedAt
from .answer_model import Answer


class Question(Base, MixinCreatedAt):

    text: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete",
    )
