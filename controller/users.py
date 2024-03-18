from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, HTTPException, Response
from service.user import UserModel
from utils.response import standard_response
from type.user import login_interface, login_info

users_router = APIRouter()
users_service = UserModel()


@users_router.post("/")
@standard_response
async def create_project(request: Request, user: login_interface) -> int:
    results = users_service.add_user(obj=user)
    return results


@users_router.post("/login")
@standard_response
async def create_project(request: Request, response: Response, user: login_info):
    results = users_service.user_register(obj=user)
    response.set_cookie(key="token", value=results)
    return "ok"
