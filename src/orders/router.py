from fastapi import APIRouter,Depends,status,HTTPException
from src.utils.helpers import is_authenticated
from src.orders.dtos import OrderCreate,OrderUpdate,OrderStatusUpdate
from sqlalchemy.orm import Session
from src.orders import controllers
from src.users.models import UserModel
from src.utils.db import get_db


order_router=APIRouter(prefix="/orders",tags=['orders'])

@order_router.get('/')
async def hello():
    return {"message":"hello orders"}
@order_router.post('/new_order',status_code=status.HTTP_201_CREATED)
def place_order(order:OrderCreate,db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return  controllers.place_order(order,db,user)
@order_router.get('/all_orders')
def get_all_orders(db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.get_all_orders(db,user)

@order_router.get('/single_order/{order_id}')
def get_single_order(order_id:int,db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.get_single_order(order_id,db,user)

@order_router.get('/user/order')
def current_user_orders(db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.get_current_user_orders(db,user)

@order_router.get('/user/order/{order_id}')
def get_user_order(order_id:int,db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.get_user_single_order(order_id,db,user)

@order_router.put('/order/update/{order_id}')
def update_order(body:OrderUpdate,order_id:int,db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.update_orders(body,order_id,db,user)

@order_router.put('/order/status/{order_id}')
def update_order_status(body:OrderStatusUpdate,order_id:int,db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.update_order_status(body,order_id,db,user)

@order_router.delete('/order/delete/{order_id}')
def delete_order(order_id:int,db=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controllers.delete_order(order_id,db,user)

@order_router.get('/order')
def testing_git():
    pass