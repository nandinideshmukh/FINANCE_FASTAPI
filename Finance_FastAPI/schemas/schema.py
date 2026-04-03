from pydantic import BaseModel,EmailStr,Field,field_validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "viewer" 
    full_name: Optional[str] = None
    
    @field_validator('role')
    def validate_type(cls, v):
        if v not in ['admin', 'analyst','viewer']:
            raise ValueError('role can be "viewer",  "admin" or "analyst"')
        return v # 


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str
    status: str
    created_at: datetime

class RecordCreate(BaseModel):
    type: str 
    amount: float = Field(..., gt=0, description="Amount must be positive")
    category: str 
    date: datetime
    description: Optional[str] = Field(None, max_length=500)
    
    
class RecordUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, max_length=500)
    
    @field_validator('type')
    def validate_type(cls, v):
        if v is not None:  
            v_upper = v.upper()
            if v_upper not in ['INCOME', 'EXPENSE']:
                raise ValueError('Type must be "INCOME" or "EXPENSE"')
            return v_upper
        return v
    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @field_validator('category')
    def validate_category(cls, v):
        if v is not None:  
            valid_categories = ["RENT", "GROCERIES", "UTILITIES", "SALES", "LOAN", "ASSETS", "OTHER"]
            v_upper = v.upper()
            if v_upper not in valid_categories:
                raise ValueError(f"Category must be one of: {valid_categories}")
            return v_upper
        return v



class RecordResponse(BaseModel):
    id: int
    user_id: int
    type: str
    amount: float
    category: str
    date: datetime
    description: Optional[str]
    created_at: datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse