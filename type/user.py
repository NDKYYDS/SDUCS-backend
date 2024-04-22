from pydantic import BaseModel, ConfigDict, field_serializer, Field
from typing import List, Optional
from datetime import datetime
from utils.times import getMsTime


class login_interface(BaseModel):
    username: str = None
    password: str = None
    role: int
    phone: str
    email: str
    gender: int


class login_info(BaseModel):
    username: str
    password: str


class user_opt(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )
    id: int
    username: str
    password: str
    role: int
    phone: str
    email: str
    gender: int
    is_delete: int
