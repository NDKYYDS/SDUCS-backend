import os
from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Response, \
    UploadFile, File
from service.goods import GoodsModel
from utils.response import standard_response, makePageResult
from utils.auther_login import auth_login
from fastapi.responses import FileResponse
from type.goods import goods_register
from type.page import page

goods_router = APIRouter()
goods_service = GoodsModel()


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
