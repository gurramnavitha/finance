from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models, dependencies

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_admin)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(current_user: models.User = Depends(dependencies.get_current_active_user)):
    return current_user
