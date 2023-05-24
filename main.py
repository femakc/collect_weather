import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi_utils.tasks import repeat_every

from api.handlers import cw_router
from city.collect_city_weather import collect_weather
from city.collect_city import collect_city_info
from city.exceptions import UvicornError
from logger_config import cw_logger as logger
from settings import API_PREFIX, API_TITLE, HOST, PORT, ROUTER_TAGS


def create_app() -> FastAPI:
    app = FastAPI(title=API_TITLE, debug=False)
    app.logger = logger

    @app.on_event("startup")
    async def start_collect_city() -> None:
        tasks = [
            asyncio.create_task(collect_city_info()),
        ]
        await asyncio.wait(tasks)

    @app.on_event("startup")
    @repeat_every(seconds=60 * 60)
    async def repeat_collect() -> None:
        await collect_weather()

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
    except UvicornError as error:
        logger.exception(error)


if __name__ == '__main__':
    main()
