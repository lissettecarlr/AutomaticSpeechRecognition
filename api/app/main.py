from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse



import logging
logger = logging.getLogger(__name__)

app = FastAPI()
logger.info(f"API服务已启动")

# 引入路由
from v1.demo import router as demo_router
app.include_router(demo_router, prefix="/api", tags=["demo"])

from v1.aliapi_paraformer_asr import router as asr_router
app.include_router(asr_router, prefix="/v1", tags=["asr"])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return PlainTextResponse("")


@app.get("/")
async def root():
    return f"服务已部署"

# 请求错误
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP 错误: {exc}")
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

# 请求数据验证错误
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )