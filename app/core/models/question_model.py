from typing import TYPE_CHECKING
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixin_model import MixinCreatedAt

if TYPE_CHECKING:
    from . import Answer


class Question(Base, MixinCreatedAt):

    text: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete",
    )
