# routes/record_routes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from db.create_db import get_db
from utils.utils import get_current_user
from models.finance_model import User
from schemas.schema import RecordCreate, RecordUpdate, RecordResponse
from services.records import RecordService

router = APIRouter(prefix="/records", tags=["Records"])

@router.post("/", response_model=RecordResponse)
async def create_record(record_data: RecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return  RecordService.create_record(db, record_data, current_user)

@router.get("/")
async def get_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),search:str = None):
    return  RecordService.view_records(db, current_user, skip, limit,search)

@router.get("/{record_id}", response_model=RecordResponse)
async def get_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return  RecordService.get_record(db, record_id, current_user)

@router.put("/{record_id}", response_model=RecordResponse)
async def update_record(record_id: int, record_data: RecordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return  RecordService.update_record(db, record_id, record_data, current_user)

@router.delete("/{record_id}")
async def delete_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return   RecordService.delete_record(db, record_id, current_user)

@router.get("/filter/")
async def filter_records(
    start_date: datetime = None,
    end_date: datetime = None,
    category: str = None,
    type: str = None,
    min_amount: float = None,
    max_amount: float = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return  RecordService.filter_records(db, current_user, start_date, end_date, category, type, min_amount, max_amount)