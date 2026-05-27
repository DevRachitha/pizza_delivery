from sqlalchemy import Column,String,Integer,Boolean,Text,ForeignKey
from src.utils.db import Base
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship

class OrderModel(Base):
    __tablename__='orders'
    
    ORDER_STATUSES=(
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered')
    )
    
    PIZZA_SIZES=(
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large')
    )
    
    id=Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUSES),default="PENDING")
    pizza_size=Column(ChoiceType(choices=PIZZA_SIZES),default="SMALL")
    flavour=Column(String)
    
    user_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    user=relationship('UserModel',back_populates='orders')
    
    def __repr__(self):
        return f"<Order {self.id}>"