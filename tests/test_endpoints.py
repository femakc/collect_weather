from tests.conftest import client


async def test_smoke():
    """Smoke Test"""
    response = client.get("/api")
    assert response.status_code == 200

# TODO Запись в БД и проверка того что записали
    # async with async_session() as session: