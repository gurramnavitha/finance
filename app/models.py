from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    Admin = "Admin"
    Analyst = "Analyst"
    Viewer = "Viewer"

class RecordTypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.Viewer)
    status = Column(String(20), default="active")

    records = relationship("Record", back_populates="creator")

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(RecordTypeEnum), nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    description = Column(String(255))
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="records")
