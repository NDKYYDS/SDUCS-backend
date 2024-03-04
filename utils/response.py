import functools
from datetime import datetime
from typing import Callable

from starlette.responses import JSONResponse

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


