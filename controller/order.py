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
async def create_order(obj: order_add, user=Depends(auth_login)) -> int:
    result = order_server.add_order(obj=obj, user_id=user)
    return result
