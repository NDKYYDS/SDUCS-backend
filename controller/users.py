from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Response, Depends
from service.user import UserModel
from type.page import page
from utils.response import standard_response, user_standard_response, makePageResult
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


@users_router.get("/list")
@standard_response
async def create_project(request: Request, Check_st: int = Query(description="状态"),
                         pageNow: int = Query(description="页码", gt=0),
                         pageSize: int = Query(description="每页数量", gt=0), user=Depends(auth_login)):
    Page = page(pageNow=pageNow, pageSize=pageSize)
    tn, res = users_service.get_user_list_by_state(state=Check_st, Page=Page,user=user)
    return makePageResult(pg=Page, tn=tn, data=res)

@users_router.put("/state")
@standard_response
async def create_project(request: Request, New_st: int = Query(description="状态"),
                         User_id: int = Query(description="页码", gt=0),
                         user=Depends(auth_login)):
    return users_service.update_state_by_user_id(user_id=User_id,new_state=New_st,user=user)

@users_router.get("/detail")
@standard_response
async def get_detail(request: Request, check_who: int, user_id=Depends(auth_login)):
    if check_who != -1:
        user_id = check_who
    # print(user_id)
    # print("daole")
    return users_service.user_detail(user_id)
