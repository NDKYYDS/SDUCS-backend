import hashlib
import os
import shutil
from typing import List
from utils.times import getMsTime
from fastapi import HTTPException, Response, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
from model.db import dbSession, dbSessionread
from model.user import Goods
from type.goods import goods_register, goods_opt
from datetime import datetime
from type.page import page, dealDataList


def save_uploaded_images(files: List[UploadFile], goods_name: str) -> List[str]:
    image_paths = []
    for file in files:
        dir_path = os.path.join("D:/sducs_date", goods_name)
        os.makedirs(dir_path, exist_ok=True)  # 确保文件夹存在
        file_path = os.path.join(dir_path, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_paths.append(file_path)
    return image_paths


class GoodsModel(dbSession, dbSessionread):
    def add_goods(self, obj: goods_register, file: List[UploadFile]):
        obj_dict = jsonable_encoder(obj)
        obj_add = Goods(**obj_dict)
        image_paths = save_uploaded_images(file, obj.name + str(getMsTime(datetime.now())))
        obj_add.image_src = ','.join(image_paths)
        print(obj_add.image_src)
        print(image_paths)
        obj_add.check_status = 0
        with self.get_db() as session:
            obj_add.is_delete = 0
            session.add(obj_add)
            session.commit()
            return obj_add.id

    def show_list(self, Page: page):
        with self.get_db() as session:
            query = session.query(Goods)
            total_count = query.count()  # 总共
            # 执行分页查询
            data = query.offset(Page.offset()).limit(Page.limit()).all()  # .all()
            print(type(data))
            data = dealDataList(data, goods_opt, {"is_check"})
            return total_count, data
