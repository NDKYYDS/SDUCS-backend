from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, field_serializer, Field
from typing import List, Optional
from datetime import datetime
from utils.times import getMsTime


class order_add(BaseModel):
    user_id: int = None
    good_id: int
    shipping_status: int = 0
    count: int
    origin: str
    destination: str


class order_opt(order_add):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
    )
    id: int
