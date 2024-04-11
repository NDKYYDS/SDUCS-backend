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
async def create_project(request: Request, file: List[UploadFile], origin: str = Query(), description: str = Query(),
                         user=Depends(auth_login)) -> int:
    goods = goods_register(name=request.headers['name'],
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


@goods_router.put("/status/{good_id}")
@standard_response
async def set_goods_status(request: Request, good_id: int, old_status: int, new_status: int,
                           user=Depends(auth_login)):  # ,user=Depends(auth_login)):
    status_change = Goods_Status_Change(old_status, new_status)
    # user = 1
    if user_service.is_admin(user):
        return goods_service.change_check_status(good_id, status_change)
    else:
        raise HTTPException(status_code=403, detail="Forbidden: You are not an admin")
