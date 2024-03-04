from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    VARCHAR,
    ForeignKey, Date, Index, Float, event, func,
)

from model.db import Base


class User(Base):  # 用户表
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    username = Column(VARCHAR(32), nullable=False, unique=True, comment='用户名')  # 用户名，非空，唯一
    password = Column(VARCHAR(128), nullable=False, comment='密码')  # 密码，非空