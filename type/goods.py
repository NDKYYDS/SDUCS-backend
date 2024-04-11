from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime
from utils.times import getMsTime


class goods_register(BaseModel):
    name: str
    price: int
    origin: str
    description: str


class goods_opt(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )
    id: int
    name: str
    user_id: int
    price: int
    image_src: str
    check_status: int


class Goods_Status_Change():
    def __init__(self,old,new):
        self.old_status=old
        self.new_status=new
    old_status: int
    new_status: int
