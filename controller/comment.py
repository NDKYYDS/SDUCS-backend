from fastapi import APIRouter, Query, Depends
from flask import Request

from service.comment import CommentModel
from type.comment import comment_interface
from type.page import page
from utils.auther_login import auth_login
from utils.response import standard_response, makePageResult

comment_router = APIRouter()
comment_service = CommentModel()


@comment_router.post("/")
@standard_response
async def create_project(comment: comment_interface, user_id=Depends(auth_login),
                         good_id: int = Query()) -> int:
    print("GYH1")
    print(good_id)
    print(user_id)
    print(comment.comment_str)
    print("GYH2")
    results = comment_service.add_comment(user_id=user_id, good_id=good_id, obj=comment)

    return results


@comment_router.delete("/delete")
@standard_response
async def delete_comment(comment_id: int,
                         user_id=Depends(auth_login)):
    return comment_service.delete_comment(comment_id, user_id)


@comment_router.get("/list")
@standard_response
async def show_comment_list(pageNow: int = Query(description="页码", gt=0),
                            pageSize: int = Query(description="每页数量", gt=0),
                            goods_id: int = Query()):
    print("GYH")
    Page = page(pageNow=pageNow, pageSize=pageSize)
    tn, res = comment_service.show_list(goods_id=goods_id, p=Page)
    return makePageResult(pg=Page, tn=tn, data=res)


@comment_router.get("/list_userId")
@standard_response
async def good_list_user(
        pageNow: int = Query(description="页码", gt=0),
        pageSize: int = Query(description="每页数量", gt=0),
        goods_id: int = Query(),
        user_id=Depends(auth_login)):
    Page = page(pageNow=pageNow, pageSize=pageSize)
    tn, res = comment_service.show_list_userid(user_id=user_id, good_id=goods_id, p=Page)
    return makePageResult(pg=Page, tn=tn, data=res)


@comment_router.post("/change")
@standard_response
async def comment_change(
        new_comment: comment_interface,
        comment_id: int = Query()
):
    return comment_service.change_comment(comment_id=comment_id, comment=new_comment)
