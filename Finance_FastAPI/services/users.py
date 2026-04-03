from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from models.finance_model import User,UserStatus
from dotenv import load_dotenv
import os
from sqlalchemy.exc import SQLAlchemyError
from schemas.schema import UserCreate, LoginRequest


load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TIME_HOURS"))
        SECRET_KEY = os.getenv("SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")
        
        if not SECRET_KEY or not ALGORITHM:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT configuration missing"
            )
        
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed"
            )
    
    @staticmethod
    def register(db: Session, user_data: UserCreate):
        # unique is email
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        new_user = User(
            email=user_data.email,
            password_hash=AuthService.hash_password(user_data.password),
            full_name=user_data.full_name,
            status=UserStatus.ACTIVE,
            role = user_data.role
        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error during registration"
            )
        
        access_token = AuthService.create_access_token(
            data={"sub": new_user.email, "user_id": new_user.id, "role": new_user.role}
        )
        
        return {
            
            "access_token": access_token,
            "status_code": status.HTTP_201_CREATED,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "full_name": new_user.full_name,
                "role": new_user.role,
                "status": new_user.status,
                "created_at": new_user.created_at                
            }
        }
    
    @staticmethod
    def login(db: Session, login_data: LoginRequest):
        try:
            user = db.query(User).filter(User.email == login_data.email).first()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error during login"
            )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if user.status == UserStatus.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Please contact admin."
            )
        
        if not AuthService.verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        access_token = AuthService.create_access_token(
            data={"sub": user.email, "user_id": user.id, "role": user.role}
        )
        
        return {
            "access_token": access_token,
            "status_code": status.HTTP_200_OK,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at
            }
        }