from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from models.finance_model import Record, User, TransactionType

class DashboardService:
    
    @staticmethod
    def get_summary(db: Session, current_user: User):
        
        query = db.query(Record)
        
        total_income = query.filter(Record.type == TransactionType.INCOME).with_entities(func.sum(Record.amount)).scalar() or 0
        total_expense = query.filter(Record.type == TransactionType.EXPENSE).with_entities(func.sum(Record.amount)).scalar() or 0
        total_records = query.with_entities(func.count(Record.id)).scalar() or 0
        
        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_balance": float(total_income - total_expense),
            "total_records": total_records
        }
    
    @staticmethod
    def get_category_breakdown(db: Session, current_user: User):
        query = db.query(Record)
        
        results = query.with_entities(
            Record.category, 
            func.sum(Record.amount).label('total'),
            func.count(Record.id).label('count')
        ).group_by(Record.category).all()
        
        total_spent = query.filter(Record.type == TransactionType.EXPENSE).with_entities(func.sum(Record.amount)).scalar() or 1
        
        return [
            {
                "category": r.category,
                "total": float(r.total),
                "count": r.count,
                "percentage": float((r.total / total_spent) * 100) if total_spent > 0 else 0
            }
            for r in results if r.category
        ]
    
    @staticmethod
    def get_recent_activity(db: Session, current_user: User, limit: int = 5):
        """Get recent transactions for dashboard"""
        query = db.query(Record)
        
        recent = query.order_by(Record.date.desc()).limit(limit).all()
        
        return [
            {
                "id": r.id,
                "amount": r.amount,
                "type": r.type,
                "category": r.category,
                "date": r.date,
                "description": r.description
            }
            for r in recent
        ]
    
    @staticmethod
    def get_monthly_trends(db: Session, current_user: User, year: int = None):
        """Get monthly income/expense trends"""
        from sqlalchemy import extract
        
        if year is None:
            year = datetime.now().year
        
        query = db.query(Record)
        
        query = query.filter(extract('year', Record.date) == year)
        
        monthly_data = []
        for month in range(1, 13):
            month_query = query.filter(extract('month', Record.date) == month)
            
            income = month_query.filter(Record.type == "INCOME").with_entities(func.sum(Record.amount)).scalar() or 0
            expense = month_query.filter(Record.type == "EXPENSE").with_entities(func.sum(Record.amount)).scalar() or 0
            # print(f"\nTransactionType.INCOME.value = '{TransactionType.INCOME.value}'")
            # print(f"TransactionType.EXPENSE.value = '{TransactionType.EXPENSE.value}'")
            
            monthly_data.append({
                "month": month,
                "month_name": datetime(year, month, 1).strftime('%B'),
                "income": float(income),
                "expense": float(expense),
                "net": float(income - expense)
            })
        
        return monthly_data