from db.create_db import Base
from sqlalchemy import Column,Integer,String , Float,Enum,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

class UserRole(str, enum.Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"

class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class TransactionType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    # this can be used in future if user want to transfer money between accounts 
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    
class Category(str,enum.Enum):
    RENT = "RENT"            
    GROCERIES = "GROCERIES"  
    UTILITIES = "UTILITIES"  
    SALES = "SALES"          
    LOAN = "LOAN"            
    ASSETS = "ASSETS"        
    OTHER = "OTHER"
    
class User(Base):
    
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    
    
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)    
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    records = relationship("Record", back_populates="user", cascade="all, delete-orphan")


class Record(Base):
    
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    category  = Column(Enum(Category), nullable=False)
    
    date = Column(DateTime, nullable=False, index=True)
    description = Column(String)
    
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    user = relationship("User", back_populates="records", lazy="joined")
    
    
    