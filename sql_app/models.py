"""Description the models of app's database."""
# pylint: disable=R0903
from typing import List, Optional
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime
)
from sqlalchemy.orm import relationship, Mapped, declarative_base, DeclarativeMeta, mapped_column

Base: DeclarativeMeta = declarative_base()


# pylint: disable=E0601
class User(Base):
    """Represents a user in the system."""

    __tablename__ = 'users'
    __table_args__ = {'schema': 'mm'}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)

    profile: Mapped['Profile'] = relationship(back_populates='user')


class Profile(Base):
    """Represents a profile associated with a user."""

    __tablename__ = 'profiles'
    __table_args__ = {'schema': 'mm'}

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('mm.users.id'))

    user: Mapped['User'] = relationship(back_populates='profile')
