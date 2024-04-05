from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Response, \
    UploadFile, File
from service.order import OrderModel
from utils.response import standard_response, makePageResult
from utils.auther_login import auth_login
from type.page import page
from type.order import order_add

order_router = APIRouter()
order_server = OrderModel()


@order_router.post("/")
@standard_response
async def create_order(obj: order_add, user=Depends(auth_login)) -> int:
    result = order_server.add_order(obj=obj, user_id=user)
    return result


@order_router.get("/list")
@standard_response
async def create_order(pageNow: int = Query(description="页码", gt=0),
                       pageSize: int = Query(description="每页数量", gt=0), name: str = Query(default=None),
                       typed: int = Query(),
                       state: int = Query(),
                       user=Depends(auth_login)) -> int:
    Page = page(pageNow=pageNow, pageSize=pageSize)
    tn, result = order_server.get_order_by_user_id(state=state, typed=typed, name=name, Page=Page, user_id=user)
    return makePageResult(pg=Page, tn=tn, data=result)


@order_router.put("/delieve")
@standard_response
async def create_order(order_id: int = Query(),
                       user=Depends(auth_login)) -> int:
    result = order_server.delieve_order_by_id(good_id=order_id, user_id=user)
    return result


@order_router.put("/receive")
@standard_response
async def create_order(order_id: int = Query(),
                       user=Depends(auth_login)) -> int:
    result = order_server.receive_order_by_id(good_id=order_id, user_id=user)
    return result
