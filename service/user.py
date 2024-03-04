from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User
from type.user import login_interface


class UserModel(dbSession, dbSessionread):
    def add_user(self, obj: login_interface):  # 管理员添加一个用户(在user表中添加一个用户)
        obj_dict = jsonable_encoder(obj)
        obj_add = User(**obj_dict)
        with self.get_db() as session:
            session.add(obj_add)
            session.commit()
            return obj_add.id
