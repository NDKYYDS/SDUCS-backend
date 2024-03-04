from datetime import datetime

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from main import app
from utils.times import getMsTime


@app.exception_handler(HTTPException)  # 自定义HttpRequest 请求异常
async def http_exception_handle(request, exc):
    response = JSONResponse({
        "code": exc.status_code,
        "message": str(exc.detail),
        "data": None,
        "timestamp": getMsTime(datetime.now())
    }, status_code=exc.status_code)
    return response


@app.exception_handler(RequestValidationError)
async def request_validatoion_error(request, exc):
    try:
        message = str(exc.detail)
    except:
        try:
            message = str(exc.raw_errors[0].exc)
        except:
            message = "请求错误"
    response = JSONResponse({
        "code": 400,
        "message": message,
        "data": None,
        "timestamp": getMsTime(datetime.now())
    }, status_code=400)
    return response


@app.exception_handler(Exception)
async def request_validatoion_error(request, exc):
    try:
        message = str(exc)
    except:
        message = None
    response = JSONResponse({
        "code": 500,
        "message": "内部错误",
        "data": message,
        "timestamp": getMsTime(datetime.now())
    }, status_code=500)
    return response