from sqlalchemy import create_engine

from const import SQLALCHEMY_DATABASE_URL_MASTER
from model.user import User, Goods, Order, Session,Comment

# 这里需要引入所有使用 Base 的 Model

create_table_list = [
    User,
    Goods,
    Order,
    Session,
    Comment
]


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URL_MASTER)
    for tb in create_table_list:
        tb.__table__.create(bind=engine, checkfirst=True)
