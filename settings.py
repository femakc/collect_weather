import os

from dotenv import load_dotenv

load_dotenv()

X_API_KEY = os.environ.get("X_API_KEY")

KELVIN_TO_CELSIUS = -271.15

BASE_URL = os.environ.get("BASE_URL")

API_KEY = os.environ.get("API_KEY")

API_TITLE = "Collect_weather"

ROUTER_TAGS = ["cwAPI"]

API_PREFIX = "/api"

HOST = "0.0.0.0"

PORT = 8000

POSTGRES_URL = os.environ.get(
    "POSTGRES_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres",
)