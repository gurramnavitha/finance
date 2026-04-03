from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models, dependencies

router = APIRouter()

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_summary(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_viewer)
):
    return crud.get_dashboard_summary(db)

@router.get("/category/{record_type}", response_model=List[schemas.CategorySummary])
def get_category_summary(
    record_type: schemas.RecordTypeEnum,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.require_viewer)
):
    return crud.get_category_summary(db, record_type.value)
