import hashlib
import os
import shutil
from typing import List

from sqlalchemy.orm import joinedload

from utils.times import getMsTime
from fastapi import HTTPException, Response, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
from model.db import dbSession, dbSessionread
from model.user import Order, Goods
from datetime import datetime
from type.order import order_add, order_opt
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

    def get_order_by_user_id(self, state: int, typed: int, name: str, Page: page, user_id: int):
        with self.get_db() as session:
            subquery = session.query(Goods).subquery()
            query = session.query(Order, subquery.c). \
                outerjoin(subquery,
                          Order.good_id == subquery.c.id)
            if typed == 0:
                query = query.filter(Order.user_id == user_id)
            else:
                query = query.filter(subquery.c.user_id == user_id)
            query = query.filter(Order.shipping_status == state)
            if name:
                query = query.filter(subquery.c.name.like(f"%{name}%"))
            total_count = query.count()  # 总共
            # 执行分页查询
            data = query.offset(Page.offset()).limit(Page.limit()).all()  # .all()
            listd = []
            for da in data:
                corder = order_opt.model_validate(da[0])
                corder = corder.model_dump()
                corder['name'] = da[3]
                listd.append(corder)
            return total_count, listd

    def delieve_order_by_id(self, good_id: int, user_id: int):
        with self.get_db() as session:
            subquery = session.query(Goods).subquery()
            query = session.query(Order, subquery.c). \
                outerjoin(subquery,
                          Order.good_id == subquery.c.id)
            query = query.filter(Order.id == good_id, subquery.c.user_id == user_id, Order.shipping_status == 0).first()
            if query is not None:
                session.query(Order).filter(Order.id == good_id).update(
                    {'shipping_status': 1})
            session.commit()
            return "OK"

    def receive_order_by_id(self, good_id: int, user_id: int):
        with self.get_db() as session:
            query = session.query(Order).filter(Order.id == good_id, Order.user_id == user_id,
                                                Order.shipping_status == 1).update(
                {'shipping_status': 2})
            session.commit()
            return "OK"
