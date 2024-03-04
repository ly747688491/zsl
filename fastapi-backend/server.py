from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.env import AppConfig
from config.get_db import init_create_table
from config.get_redis import RedisUtil
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware
from module_data.controller.test_controller import testController
from utils.system_utils import logger


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{AppConfig.app_name}开始启动")
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    logger.info(f"{AppConfig.app_name}启动成功")
    yield
    await RedisUtil.close_redis_pool(app)


app = FastAPI(
    title=AppConfig.app_name,
    description=f"{AppConfig.app_name}接口文档",
    version=AppConfig.app_version,
    lifespan=lifespan,
    root_path=AppConfig.app_root_path,
)

# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)

controller_list = [{"router": testController, "tags": ["测试模块"]}, ]

for controller in controller_list:
    app.include_router(router=controller.get("router"), tags=controller.get("tags"))
