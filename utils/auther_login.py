import ast
import json
import time

import requests
from fastapi import Request, HTTPException, Depends
from model.user import Session
from service.user import UserModel

user_servrce = UserModel()


def auth_login(request: Request):  # 用来判断用户是否登录
    token = request.cookies.get("TOKEN")
    if token is not None:
        user_id = user_servrce.get_user_by_token(token=token)
        if user_id == 0:
            raise HTTPException(
                status_code=401,
                detail="用户未登录"
            )
        else:
            return user_id
    else:
        raise HTTPException(
            status_code=401,
            detail="用户未登录"
        )
