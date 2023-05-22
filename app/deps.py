from app.services.PolygonService import PolygonService
from app.services.StocksService import StocksService
from app.services.UserService import UserService
from database import async_session
from settings import Settings
from polygon import RESTClient

settings = Settings()
api_key = settings.API_KEY

client = RESTClient(api_key=api_key)
# client = RESTClient(api_key=api_key, verbose=True, trace=True)

global_context = {
    "polygon_client": client,
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


async def get_user_service():
    async with async_session() as session:
        async with session.begin():
            yield UserService(session)
