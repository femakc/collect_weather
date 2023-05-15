import asyncio

from city.collect_city import collect_city_info, collect_city_info_second
from logger_config import cw_logger as logger

from city_geo import collect_weather

LAUNCH_OPTIONS = {
    "start": {
        "--city": collect_city_info,
        "--city2": collect_city_info_second,  # TODO crutch + 20 cites
        "--weather": collect_weather,
    },
}


def main(argv=None):
    if argv is None:
        logger.debug("argv is None")
        return

    func_name = argv[1:]
    try:
        logger.info(
            f"start launcher with param: {func_name[0]} {func_name[1]}"
        )
        asyncio.run(LAUNCH_OPTIONS[func_name[0]][func_name[1]]())
    except Exception as error:
        logger.exception(f"launcher failed: {error}")


if __name__ == "__main__":
    main()
