from __future__ import annotations  # resolve importação circular
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        db.String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), nullable=True)
    password_hash: Mapped[str] = mapped_column(db.String(128), nullable=False)

    role_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
