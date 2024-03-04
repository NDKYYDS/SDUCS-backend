from pydantic import BaseModel, ConfigDict, field_serializer, Field
from typing import List, Optional
from datetime import datetime
from utils.times import getMsTime


class login_interface(BaseModel):
    username: str = None
    password: str = None
