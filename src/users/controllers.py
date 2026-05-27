from src.users.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from fastapi import HTTPException,status
import jwt
from pwdlib import PasswordHash
from datetime import datetime,timedelta
from src.utils.settings import settings


password_hash=PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_user(body:UserSchema,db:Session):
    is_user=db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User name already exist")
    is_user=db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User email already exist")
    new_user=UserModel(
        username=body.username,
        email=body.email,
        hash_password=get_password_hash(body.password),
        is_active=body.is_active,
        is_staff=body.is_staff
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def login(body:LoginSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No username found")
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You entered wrong password")
    exp_time=datetime.now()+timedelta(minutes=settings.EXP_TIME)
    token=jwt.encode({'_id':user.id,'exp':exp_time},settings.SECRET_KEY,settings.ALGORITHM)
    
    return {"token":token}
    