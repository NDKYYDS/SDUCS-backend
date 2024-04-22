from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Response, Depends
from service.user import UserModel
from utils.response import standard_response, user_standard_response
from type.user import login_interface, login_info
from utils.auther_login import auth_login

users_router = APIRouter()
users_service = UserModel()


@users_router.post("/")
@standard_response
async def create_project(request: Request, user: login_interface) -> int:
    results = users_service.add_user(obj=user)
    return results


@users_router.post("/login")
@user_standard_response
async def create_project(request: Request, response: Response, user: login_info):
    results = users_service.user_register(obj=user)
    return {'message': '登录成功', 'token_header': results, 'data': True, 'code': 0}


@users_router.get("/detail")
@standard_response
async def get_detail(request: Request, check_who:int, user_id=Depends(auth_login)):
    if check_who != -1:
        user_id = check_who
    # print(user_id)
    # print("daole")
    return users_service.user_detail(user_id)
