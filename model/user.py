from datetime import datetime

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
    role = Column(Integer, nullable=False, comment='用户角色')  # 0：买家，1：买家，2：管理员
    phone = Column(VARCHAR(32), nullable=False, comment='电话号码')  # 电话号码，非空
    email = Column(VARCHAR(32), comment='邮箱')  # 邮箱
    gender = Column(Integer, comment='性别')  # 性别
    is_delete = Column(Integer, nullable=False, comment="是否注销")  # 是否注销


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    name = Column(VARCHAR(32), nullable=False, comment='商品名称')  # 产品名称
    price = Column(Integer, nullable=False, comment="商品价格")  # 商品价格
    image_src = Column(VARCHAR(300), nullable=False, unique=True, comment='商品图片路径')  # 商品图片路径，非空，图片存放在服务器端，也就是后端电脑中
    check_status = Column(Integer, nullable=False, comment='审核状态')  # 审核状态 非空


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')  # 主键
    user_id = Column(Integer, comment='用户ID')  # 用户ID
    good_id = Column(Integer, comment='商品ID')  # 商品ID
    shipping_status = Column(Integer, nullable=False, comment='发货状态')  # 商品的发货状态  0表示未发货，1表示发货
    delivery_status = Column(Integer, nullable=False, comment='收货状态')  # 商品的收货状态，0表示未收货，1表示收货。
    transaction_status = Column(Integer, nullable=False, comment="交易状态")  # 0交易中，1交易成功，2交易失败
    count = Column(Integer, nullable=False, comment="交易数量")
    origin = Column(VARCHAR(64), nullable=False, comment='发货地')
    destination = Column(VARCHAR(64), nullable=False, comment='收货地')


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, comment="主键")
    user_id = Column(Integer, nullable=False, unique=False, comment="用户id")  # 用户ID，用于关联用户信息
    token = Column(VARCHAR(128), nullable=False, unique=True)  # 会话令牌，用于识别会话
    created_at = Column(DateTime, default=datetime.now)  # 会话创建时间
    # 其他可能需要存储的会话信息，如过期时间、用户代理等

