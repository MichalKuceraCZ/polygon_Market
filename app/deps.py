from app.services.PolygonService import PolygonService
from app.services.StocksService import StocksService
from database import async_session
from settings import Settings

settings = Settings()
api_key = settings.API_KEY


global_context = {
    "api_key": api_key,
}


async def get_polygon_service():
    async with async_session() as session:
        async with session.begin():
            context = {**global_context, "session": session}

            yield PolygonService(context)


async def get_stocks_service():
    async with async_session() as session:
        async with session.begin():
            context = {**global_context, "session": session}

            yield StocksService(context)
