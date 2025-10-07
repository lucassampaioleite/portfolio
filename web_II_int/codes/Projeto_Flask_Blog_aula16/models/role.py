from __future__ import annotations  # resolve importação circular
from extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
