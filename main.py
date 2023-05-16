import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi_utils.tasks import repeat_every

from api.handlers import cw_router
from city.city_geo import collect_weather
from city.collect_city import collect_city_info, collect_city_info_second
from logger_config import cw_logger as logger
from settings import API_PREFIX, API_TITLE, HOST, PORT, ROUTER_TAGS


def create_app() -> FastAPI:
    app = FastAPI(title=API_TITLE, debug=False)
    app.logger = logger

    @app.on_event("startup")
    async def start_collect_city():
        try:
            tasks = [
                asyncio.create_task(collect_city_info()),
                asyncio.create_task(collect_city_info_second()),
            ]
            await asyncio.wait(tasks)
        except Exception as e:
            logger.exception("collect start failed %s ", e)

    @app.on_event("startup")
    @repeat_every(seconds=60 * 1)
    async def repeat_collect():
        try:
            tasks = [
                asyncio.create_task(collect_weather()),
            ]
            await asyncio.wait(tasks)
        except Exception as e:
            logger.exception("repeat collect start failed %s ", e)
    return app


app = create_app()

main_api_router = APIRouter()

main_api_router.include_router(
    cw_router,
    prefix=API_PREFIX,
    tags=ROUTER_TAGS
)
app.include_router(main_api_router)


def main():
    try:
        uvicorn.run(app, host=HOST, port=PORT)
    except Exception as e:
        logger.exception("uvicorn failed %s ", e)


if __name__ == '__main__':
    main()
