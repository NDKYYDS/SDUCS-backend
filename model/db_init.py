from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from const import SQLALCHEMY_DATABASE_URL_MASTER
from model.user import User, Goods, Order, Session, Comment
from service.user import hash_password
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
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    for tb in create_table_list:
        tb.__table__.create(bind=engine, checkfirst=True)
    user_data = {
        "username": "admin",
        "password": hash_password("123456"),
        "role": 2,
        "phone": "1",
        "email": "1",
        "gender": 1,
        "state": 1,
        "is_delete": 0
    }
    new_user = User(**user_data)
    session.add(new_user)
    session.commit()
    session.close()
