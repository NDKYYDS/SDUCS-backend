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

updates_router = APIRouter()


@updates_router.get("/uploads/{file_name}")
async def get_uploaded_file(file_name: str):
    file_path = os.path.join("uploads", file_name)
    print(file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
