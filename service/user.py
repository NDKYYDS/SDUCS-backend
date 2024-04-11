import hashlib

from fastapi import HTTPException, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, join, update, desc
import model.user
from model.db import dbSession, dbSessionread
from model.user import User
from model.user import Session as se
from type.user import login_interface, login_info


def hash_password(password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


class UserModel(dbSession, dbSessionread):
    def add_user(self, obj: login_interface):  # 管理员添加一个用户(在user表中添加一个用户)
        # 加密密码
        obj.password = hash_password(obj.password)
        obj_dict = jsonable_encoder(obj)
        obj_add = User(**obj_dict)
        print(obj.password)
        with self.get_db() as session:
            obj_add.is_delete = 0
            project = session.query(User).filter(User.username == obj_add.username).first()
            if project is not None:
                raise HTTPException(status_code=400, detail="Username already registered")
            session.add(obj_add)
            session.commit()
            return obj_add.id

    def user_register(self, obj: login_info):
        obj.password = hash_password(obj.password)
        print(obj.password)
        with self.get_db() as session:
            user = session.query(User).filter(User.username == obj.username,
                                              User.password == obj.password).first()
            if user is None:
                raise HTTPException(status_code=401, detail="Incorrect username or password")
            token_current = hash_password(user.username + user.password)
            session_current = session.query(se).filter(se.user_id == user.id).first()
            if session_current is None:
                sess = se(user_id=user.id, token=token_current)
                session.add(sess)
                session.commit()
            # response.set_cookie(key="user", value=token_current)
            return token_current

    def get_user_by_token(self, token: str):
        with self.get_db() as session:
            use = session.query(se).filter(se.token == token).first()
            if session is None:
                return 0
            else:
                return use.user_id

    def is_admin(self, userid):
        with self.get_db() as session:
            theUser = session.query(User).filter(User.id == userid).first()
            return theUser.role == 2