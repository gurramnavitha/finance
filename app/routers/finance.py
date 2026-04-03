from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud, models, dependencies

router = APIRouter()

@router.post("/", response_model=schemas.RecordResponse)
def create_record(
    record: schemas.RecordCreate, 
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_admin)
):
    return crud.create_record(db=db, record=record, user_id=current_user.id)

@router.get("/", response_model=List[schemas.RecordResponse])
def read_records(
    skip: int = 0, limit: int = 100,
    record_type: Optional[schemas.RecordTypeEnum] = None,
    category: Optional[str] = None,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_analyst)
):
    type_val = record_type.value if record_type else None
    records = crud.get_records(db, skip=skip, limit=limit, record_type=type_val, category=category)
    return records

@router.put("/{record_id}", response_model=schemas.RecordResponse)
def update_record(
    record_id: int, 
    record: schemas.RecordUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_admin)
):
    db_record = crud.update_record(db, record_id, record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_admin)
):
    success = crud.delete_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}
