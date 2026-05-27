from sqlalchemy import Column,String,Integer,Boolean,Text
from src.utils.db import Base
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__='users'
    
    id=Column(Integer,primary_key=True)
    username=Column(String(25),unique=True)
    email=Column(String,unique=True)
    hash_password=Column(Text,nullable=True)
    is_staff=Column(Boolean,default=False)
    is_active=Column(Boolean,default=False)
    orders=relationship('OrderModel',back_populates='user')
    
    def __repr__(self):
        return f"<User {self.username}"