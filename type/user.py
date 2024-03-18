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
