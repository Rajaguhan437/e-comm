from logger import logger
import time
from fastapi import Request, Cookie, APIRouter


async def logger_middleware(request: Request, call_next):
    print("Starting API...")
    start_time = time.time()
    
    log_dict = { 
        'url': request.url.path,
        'method': request.method,
    }
    logger.info(log_dict)

    response = await call_next(request)
    processing_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(processing_time)
    response.set_cookie(key="mycookie", value="000000000", max_age=3600, path="/", secure=False)
    
    return response