from fastapi import FastAPI
from src.orders.router import order_router
from src.users.router import auth_router
from src.utils.db import Base,engine
from src.orders.models import OrderModel
from src.users.models import UserModel

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)

app=FastAPI()
app.include_router(order_router)
app.include_router(auth_router)