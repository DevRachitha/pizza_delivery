from pydantic import BaseModel,ConfigDict
from typing import Optional

class OrderCreate(BaseModel):
    id:Optional[int]=None
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    # user_id:Optional[int]=None
    flavour:str
    
    model_config=ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example':{
                'quantity':1,
                'order_status':'PENDING',
                'pizza_size':'SMALL',
                'flavour':'hot and spicy',
                'user_id':False,
                
            }}
    )

class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    pizza_size: Optional[str] = None
    flavour: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    order_status: str
    
    model_config = ConfigDict(from_attributes=True)