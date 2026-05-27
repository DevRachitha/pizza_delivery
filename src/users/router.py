from fastapi import APIRouter,Depends,status,HTTPException,Request
from src.users.dtos import UserSchema,LoginSchema
from src.utils.db import get_db
from src.users import controllers
from sqlalchemy.orm import Session
from src.utils import helpers
auth_router=APIRouter(prefix="/auth",tags=['auth'])

@auth_router.post('/register',status_code=status.HTTP_201_CREATED)
async def create_user(body:UserSchema,db:Session=Depends(get_db)):
    return  controllers.create_user(body,db)

@auth_router.post('/login',status_code=status.HTTP_200_OK)
async def login(body:LoginSchema,db:Session=Depends(get_db)):
    return  controllers.login(body,db)

@auth_router.get('/is_auth',status_code=status.HTTP_200_OK)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return helpers.is_authenticated(request,db)