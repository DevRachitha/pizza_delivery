from src.orders.dtos import OrderCreate,OrderUpdate,OrderStatusUpdate
from sqlalchemy.orm import Session
from src.orders.models import OrderModel
from src.users.models import UserModel

from fastapi import HTTPException,status
import jwt
from pwdlib import PasswordHash
from datetime import datetime,timedelta
from src.utils.settings import settings

def place_order(body: OrderCreate, db: Session, user: UserModel):
    data = body.model_dump()

    new_order = OrderModel(
        quantity=body.quantity,
        pizza_size=body.pizza_size,
        flavour=body.flavour,
        user_id=user.id,
        order_status=body.order_status
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

def get_all_orders(db:Session,user:UserModel):
    if user.is_staff:
        orders=db.query(OrderModel).all()
        return {"orders":orders}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")

def get_single_order(order_id:int,db:Session,user:UserModel):
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized"
        )
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return {"order": order}

def get_current_user_orders(db:Session,user:UserModel):
    orders=db.query(OrderModel).filter(OrderModel.user_id == user.id).all()
    if not orders:
         return {"message": "No orders found", "orders": []}
    else:
        return {"orders":orders}
def get_user_single_order(order_id:int,db:Session,user:UserModel):
    order=db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    if order.user_id != user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    return order

def update_orders(body:OrderUpdate,order_id:int,db:Session,user:UserModel):
    order=db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    if order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not allowed to update")
    
    data = body.model_dump(exclude_unset=True)
    for field,value in data.items():
        if field in data:
         setattr(order,field,value)
         
    db.commit()
    db.refresh(order)
     
    return {"status":"Order updated sucecssfully","data":order}

def update_order_status(body:OrderStatusUpdate,order_id:int,db:Session,user:UserModel):
    order=db.query(OrderModel).filter(OrderModel.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update order status"
        )
    order.order_status=body.order_status
    db.commit()
    db.refresh(order)
            
    return {
        "status": "Order status updated successfully",
        "data": order
    }
    
def delete_order(order_id:int,db:Session,user:UserModel):
    order=db.query(OrderModel).get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Order is not available to delete")
    if order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized to delete")
    db.delete(order)
    db.commit()
    return {"message":"Order deleted successfully"}
    
        