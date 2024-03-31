import hashlib
import os
import shutil
from typing import List
from utils.times import getMsTime
from fastapi import HTTPException, Response, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
from model.db import dbSession, dbSessionread
from model.user import Order
from datetime import datetime
from type.order import order_add
from type.page import page, dealDataList


class OrderModel(dbSession, dbSessionread):
    def add_order(self, obj: order_add, user_id: int):
        obj_dict = jsonable_encoder(obj)
        obj_add = Order(**obj_dict)
        obj_add.user_id = user_id
        with self.get_db() as session:
            session.add(obj_add)
            obj.user_id = user_id
            session.commit()
            return obj_add.id
