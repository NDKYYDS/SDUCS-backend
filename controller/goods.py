import os
from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Response, \
    UploadFile, File
from service.goods import GoodsModel
from service.user import UserModel
from utils.response import standard_response, makePageResult
from utils.auther_login import auth_login
from fastapi.responses import FileResponse
from type.goods import goods_register, Goods_Status_Change
from type.page import page

goods_router = APIRouter()
goods_service = GoodsModel()
user_service = UserModel()


@goods_router.post("/")
@standard_response
async def create_project(request: Request, file: List[UploadFile], name: str = Query(), origin: str = Query(),
                         description: str = Query(),
                         user=Depends(auth_login)) -> int:
    goods = goods_register(name=name,
                           price=int(request.headers['price']),
                           origin=origin,
                           description=description)
    results = goods_service.add_goods(obj=goods, file=file, user=user)
    return results


@goods_router.get("/list")
@standard_response
async def show_goods_list(request: Request, pageNow: int = Query(description="页码", gt=0),
                          pageSize: int = Query(description="每页数量", gt=0), name: str = Query(default=None),
                          user=Depends(auth_login)):
    Page = page(pageNow=pageNow, pageSize=pageSize)
    tn, res = goods_service.show_list(Page=Page, name=name)
    return makePageResult(pg=Page, tn=tn, data=res)


@goods_router.get("/good_list_user")
@standard_response
async def good_list_user(request: Request, checkall: bool, user_id=Depends(auth_login),
                         pageNow: int = Query(description="页码", gt=0),
                         pageSize: int = Query(description="每页数量", gt=0)):
    Page = page(pageNow=pageNow, pageSize=pageSize)
    tn, res = goods_service.show_list_userid(user_id, checkall, Page)
    return makePageResult(pg=Page, tn=tn, data=res)


@goods_router.put("/status")
@standard_response
async def set_goods_status(request: Request, good_id: int, old_status: int, new_status: int,
                           user_id=Depends(auth_login)):  # ,user=Depends(auth_login)):
    status_change = Goods_Status_Change(old_status, new_status)
    if user_service.is_admin(user_id):
        return goods_service.change_check_status(good_id, status_change)
    else:
        raise HTTPException(status_code=403, detail="Forbidden: You are not an admin")


@goods_router.delete("/delete")
@standard_response
async def delete_goods(request: Request, good_id: int, user_id=Depends(auth_login)):
    return goods_service.delete_good(good_id, user_id)


# 403   没权限
# 404   没有商品
# 422   商品信息错误


@goods_router.get("/good_detail")
@standard_response
async def get_goods_detail(request: Request, good_id: int, user_id=Depends(auth_login)):
    return goods_service.get_good_detail(good_id)
