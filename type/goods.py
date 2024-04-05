from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, field_serializer, Field
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
