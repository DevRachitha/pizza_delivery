from pydantic import BaseModel,ConfigDict
from typing import Optional

class UserSchema(BaseModel):
    id:Optional[int]=None
    username:str
    email:str
    password:str
    is_staff:Optional[bool]=False
    is_active:Optional[bool]=True

    model_config=ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example':{
                'username':"rachitha",
                'email':'rachitha@gmail.com',
                'password':'password',
                'is_staff':False,
                'is_active':True
            }}
    )

class LoginSchema(BaseModel):
    username:str
    password:str