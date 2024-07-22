"""Description the models of app's database."""
# pylint: disable=R0903
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String)
from sqlalchemy.orm import relationship, Mapped, declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


# pylint: disable=E0601
class User(Base):
    """Represents a user in the system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    profile: Mapped[Profiles] = relationship("Profiles", back_populates="user")


class Profiles(Base):
    """Represents a profile associated with a user."""

    __tablename__ = "profile_med"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True, index=True)
    user_id: int = Column(Integer, ForeignKey('users.id'))

    user: Mapped[User] = relationship("User", back_populates="profile")
