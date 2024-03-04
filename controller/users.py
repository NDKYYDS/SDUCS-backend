from typing import Optional

import httpx
import requests
from fastapi import APIRouter, Depends, Query, Request, HTTPException
from service.user import UserModel
from utils.response import standard_response
from type.user import login_interface

users_router = APIRouter()
users_service = UserModel()


@users_router.post("/")
@standard_response
async def create_project(request: Request, user: login_interface) -> int:
    results = users_service.add_user(obj=user)
    return results
