from utils.utils import get_current_user,require_role
from models.finance_model import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.create_db import get_db
from schemas.schema import UserCreate, LoginRequest, LoginResponse, UserResponse
from services.users import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=LoginResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return   AuthService.register(db, user_data)

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return   AuthService.login(db, login_data)

@router.get("/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "status": current_user.status
    }

# @router.get("/admin-only")
# def admin_endpoint(current_user: User = Depends(require_role(["admin"]))):
#     return {"message": "Welcome admin!"}

# @router.get("/analyst-viewer")
# def analyst_or_viewer_endpoint(current_user: User = Depends(require_role(["analyst", "viewer"]))):
#     """Analyst and viewer can access this"""
#     return {"message": f"Hello {current_user.role}!"}