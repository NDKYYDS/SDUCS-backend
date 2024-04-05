import hashlib
import os
import shutil
import uuid
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


def save_upload_files(files: list):
    uploaded_file_paths = []
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    for file in files:
        # 生成唯一的文件名
        file_name = str(uuid.uuid4()) + "-" + file.filename
        file_path = os.path.join(upload_folder, file_name)

        # 将文件写入服务器
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_file_paths.append(file_path)

    return uploaded_file_paths


class GoodsModel(dbSession, dbSessionread):
    def add_goods(self, obj: goods_register, file: List[UploadFile], user: int):
        obj_dict = jsonable_encoder(obj)
        obj_add = Goods(**obj_dict)
        image_paths = save_upload_files(file)
        path_list = []
        base_url = "http://localhost:8000"
        for file_path in image_paths:
            # 构建文件链接
            file_name = os.path.basename(file_path)
            path_list.append(f"{base_url}/uploads/{file_name}")
        obj_add.image_src = ",".join(path_list)
        print(obj_add.image_src)
        print(image_paths)
        obj_add.check_status = 0
        obj_add.user_id = user
        with self.get_db() as session:
            obj_add.is_delete = 0
            session.add(obj_add)
            session.commit()
            return obj_add.id

    def show_list(self, name: str, Page: page):
        with self.get_db() as session:
            query = session.query(Goods).filter(Goods.check_status == 0)
            if name:
                query = query.filter(Goods.name.like(f"%{name}%"))
            total_count = query.count()  # 总共
            # 执行分页查询
            data = query.offset(Page.offset()).limit(Page.limit()).all()  # .all()
            print(type(data))
            data = dealDataList(data, goods_opt, {"is_check"})
            return total_count, data
