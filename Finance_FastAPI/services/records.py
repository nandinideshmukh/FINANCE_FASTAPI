from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from datetime import datetime
from models.finance_model import Record, User, Category
from schemas.schema import RecordCreate, RecordUpdate
from sqlalchemy.exc import SQLAlchemyError
class RecordService:
    
    @staticmethod
    def create_record(db: Session, record_data: RecordCreate, current_user: User):
        if current_user.role not in [ "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' cannot create records. Required: admin"
            )
        
        new_record = Record(
            user_id=current_user.id,
            type=record_data.type,
            amount=record_data.amount,
            category=record_data.category,
            date=record_data.date,
            description=record_data.description
        )
        try:
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while creating record"
            )
        return new_record
    
    @staticmethod
    def get_record(db: Session, record_id: int, current_user: User):
        
        if current_user.role not in ["admin", "analyst"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' cannot view records. Required: analyst or admin"
            )
        
        try:    
            record = db.query(Record).filter(Record.id == record_id).first()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while fetching record"
            )
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
            
        if current_user.role not in ["admin","analyst"] and record.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot view records"
            )
        return record

    @staticmethod
    def view_records(db: Session, current_user: User, page: int = 1, limit: int = 10, search: str = None):
        
        if limit < 1 :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page must be greater than 0"
            )
                
        if current_user.role not in ["admin", "analyst"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' cannot view records. Required: analyst or admin"
            )
        
        try:
            query = db.query(Record)
            
            
            if search:
                search_term = f"%{search}%"
                query = query.filter(Record.description.ilike(search_term))
            
            total = query.count()
            
            offset = (page - 1) * limit
            total_pages = (total + limit - 1) // limit if total > 0 else 1
            
            records = query.order_by(Record.date.desc()).offset(offset).limit(limit).all()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while fetching records"
            )
            
        
        
        
        return {
            "items": records,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    
    @staticmethod
    def update_record(db: Session, record_id: int, record_data: RecordUpdate, current_user: User):
        if current_user.role not in ["admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' cannot update records"
            )
        record = db.query(Record).filter(Record.id == record_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
        
        
        for field, value in record_data.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        try:
            db.commit()
            db.refresh(record)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while updating record"
            )
            
        
        return record
    
    @staticmethod
    def delete_record(db: Session, record_id: int, current_user: User):
        if current_user.role not in ["admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' cannot delete records"
            )
        
        record = db.query(Record).filter(Record.id == record_id).first()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found"
            )
        
        try:
            db.delete(record)
            db.commit()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while deleting record"
            )
        return {"message": "Record deleted successfully"}


    @staticmethod
    def filter_records(db: Session, current_user: User, start_date: datetime = None, 
                       end_date: datetime = None, category: str = None, 
                       type: str = None, min_amount: float = None, max_amount: float = None):
        
        if current_user.role not in ["admin", "analyst"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' cannot view records. Required: analyst or admin"
            )
        
        query = db.query(Record)
        
        if start_date:
            query = query.filter(Record.date >= start_date)
        if end_date:
            query = query.filter(Record.date <= end_date)
        if category:
            query = query.filter(Record.category == category)
        if type:
            query = query.filter(Record.type == type)
        if min_amount:
            query = query.filter(Record.amount >= min_amount)
        if max_amount:
            query = query.filter(Record.amount <= max_amount)
        
        try:
            return query.all()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while filtering records"
            )