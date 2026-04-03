from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    Admin = "Admin"
    Analyst = "Analyst"
    Viewer = "Viewer"

class RecordTypeEnum(str, Enum):
    income = "income"
    expense = "expense"

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum = RoleEnum.Viewer
    status: str = "active"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# Record Schemas
class RecordBase(BaseModel):
    amount: float
    type: RecordTypeEnum
    category: str
    date: Optional[datetime] = None
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[RecordTypeEnum] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None

class RecordResponse(RecordBase):
    id: int
    created_by: int
    date: datetime

    class Config:
        from_attributes = True

# JWT Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Dashboard Schemas
class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float

class CategorySummary(BaseModel):
    category: str
    total_amount: float
