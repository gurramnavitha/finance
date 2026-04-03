from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from .auth import get_password_hash

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        status=user.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Record CRUD
def get_records(db: Session, skip: int = 0, limit: int = 100, record_type: str = None, category: str = None):
    query = db.query(models.Record)
    if record_type:
        query = query.filter(models.Record.type == record_type)
    if category:
        query = query.filter(models.Record.category == category)
    return query.offset(skip).limit(limit).all()

def get_record(db: Session, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()

def create_record(db: Session, record: schemas.RecordCreate, user_id: int):
    db_record = models.Record(**record.model_dump(), created_by=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_record(db: Session, record_id: int, record: schemas.RecordUpdate):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not db_record:
        return None
    for key, value in record.model_dump(exclude_unset=True).items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False

# Dashboard CRUD (Analytics)
def get_dashboard_summary(db: Session):
    income = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "income").scalar() or 0.0
    expense = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "expense").scalar() or 0.0
    return {
        "total_income": income,
        "total_expenses": expense,
        "net_balance": income - expense
    }

def get_category_summary(db: Session, record_type: str):
    results = db.query(
        models.Record.category, 
        func.sum(models.Record.amount).label('total')
    ).filter(
        models.Record.type == record_type
    ).group_by(
        models.Record.category
    ).all()
    
    return [{"category": r.category, "total_amount": r.total} for r in results]
