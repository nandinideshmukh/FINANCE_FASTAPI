# routes/dashboard_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Query, Session
from db.create_db import get_db
from utils.utils import get_current_user
import datetime
from models.finance_model import User
from services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return   DashboardService.get_summary(db, current_user)

@router.get("/category-breakdown")
async def get_category_breakdown(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return   DashboardService.get_category_breakdown(db, current_user)

@router.get("/recent-activity")    
async def get_recent_activity(db: Session = Depends(get_db), current_user: User = Depends(get_current_user),limit:int = 5):
        return  DashboardService.get_recent_activity(db, current_user,limit )

@router.get("/monthly-trends")  
async def get_monthly_trends(year: int = Query(datetime.datetime.now().year),db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return DashboardService.get_monthly_trends(db, current_user, year)