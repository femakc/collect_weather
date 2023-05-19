import asyncio
from typing import Optional

from city_geo import collect_weather

from city.collect_city import collect_city_info
from logger_config import cw_logger as logger

LAUNCH_OPTIONS: dict = {
    "start": {
        "--city": collect_city_info,
        "--weather": collect_weather,
    },
}


def main(argv: Optional[list[str]] = None):
    if argv is None:
        logger.debug("argv is None")
        return

    func_name: list[str] = argv[1:]
    try:
        logger.info(
            "start launcher with param: %s %s",
            func_name[0], func_name[1]
        )
        asyncio.run(LAUNCH_OPTIONS[func_name[0]][func_name[1]]())
    except Exception as error:
        logger.exception(error)


if __name__ == "__main__":
    main()
