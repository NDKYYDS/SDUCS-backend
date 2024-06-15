from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from model.user import Comment
from model.db import dbSession, dbSessionread
from service.user import UserModel
from type.comment import comment_interface, comment_opt
from type.page import page, dealDataList
from fastapi import HTTPException

user_service = UserModel()


class CommentModel(dbSession, dbSessionread):

    def add_comment(self, user_id: int, good_id: int, obj: comment_interface):
        obj_dict = jsonable_encoder(obj)
        obj_add = Comment(**obj_dict)
        obj_add.user_id = user_id
        obj_add.good_id = good_id
        obj_add.check_status = 1
        with self.get_db() as session:
            session.add(obj_add)
            session.commit()
            return obj_add.id

    def delete_comment(self, comment_id: int, user_id: int):
        with self.get_db() as session:
            theComment = session.query(Comment).filter(Comment.id == comment_id).first()
            if theComment is None:
                raise HTTPException(status_code=404, detail="NoComment")
            try:
                theComment = session.query(Comment).filter(Comment.id == comment_id).first()
                if theComment.user_id == user_id or user_service.is_admin(user_id):
                    session.query(Comment).filter(Comment.id == comment_id).delete()
                    session.commit()
                else:
                    raise HTTPException(status_code=403, detail="NoPermission")
                return "OK"
            except SQLAlchemyError as e:
                session.rollback()  # 回滚事务
                error_msg = f"An error occurred: {str(e)}"
                return error_msg

    def show_list(self, goods_id: int, p: page):
        with self.get_db() as session:
            query = session.query(Comment).filter(Comment.check_status == 1)
            query = query.filter(Comment.good_id == goods_id)
            total_count = query.count()
            print("GYH1")
            # 执行分页查询
            data = query.offset(p.offset()).limit(p.limit()).all()  # .all()
            print(type(data))
            data = dealDataList(data, comment_opt, {"is_check"})
            return total_count, data

    def show_list_userid(self, user_id: int, good_id, p: page):
        with self.get_db() as session:
            query = session.query(Comment).filter(Comment.check_status == 1)
            query = query.filter(Comment.good_id == good_id)
            query = query.filter(Comment.user_id == user_id)
            total_count = query.count()
            # 执行分页查询
            data = query.offset(p.offset()).limit(p.limit()).all()  # .all()
            print(type(data))
            data = dealDataList(data, comment_opt, {"is_check"})
            return total_count, data

    def change_comment(self, comment_id: int, comment: comment_interface):
        comment_str = comment.comment_str
        with self.get_db() as session:
            # 执行查询操作
            comment = session.query(Comment).filter(Comment.id == comment_id).first()

            # 检查查询结果是否为空
            if comment is not None:
                # 更新操作
                session.query(Comment).filter(Comment.id == comment_id).update({'comment_str': comment_str})
                session.commit()
                return "OK"
            else:
                raise HTTPException(status_code=404, detail="No Comment")

