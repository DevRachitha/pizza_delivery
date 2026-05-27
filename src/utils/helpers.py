from fastapi import FastAPI,HTTPException,Request,status,Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
from datetime import datetime
import jwt
from src.users.models import UserModel
from src.utils.db import get_db
 ## Token Send
 
def is_authenticated(request:Request,db:Session=Depends(get_db)):
    token=request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    token=token.split(" ")[-1]
    data=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)
    user_id=data.get('_id')
    exp_time=data.get('exp')
    
    current_time=datetime.now().timestamp()
    if current_time>exp_time:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    user=db.query(UserModel).filter(UserModel.id==user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    return user