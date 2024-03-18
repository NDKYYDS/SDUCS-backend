import functools
from datetime import datetime
from typing import Callable, List

from starlette.responses import JSONResponse
from type.page import page,pageResult
from utils.times import getMsTime


def standard_response(func: Callable):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)
        return JSONResponse({
            "code": 0,
            "message": "OK",
            "data": result,
            "timestamp": getMsTime(datetime.now())
        }, status_code=200)

    return decorator


def makePageResult(pg: page, tn: int, data: List):  # 处理分页数据
    return pageResult(
        totalNum=tn,
        totalPage=(tn + pg.pageSize - 1) // pg.pageSize,
        rows=data
    ).model_dump()
