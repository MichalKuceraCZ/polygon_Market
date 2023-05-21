from sqlmodel import select

from app.data.StockAggregatesData import StockAggregatesData
from app.data.StocksData import StocksData
from app.models.StockDataModel import StockDataModel
from app.models.StockModel import StockModel


class StocksService:

    def __init__(self, context):
        self.session = context["session"]

    async def create(self, data: list[StocksData]) -> None:
        new_stocks = []

        for stock in data:
            stock_model = StockModel(
                ticker=stock["ticker"],
                name=stock["name"],
                currency_name=stock["currency_name"],
            )
            new_stocks.append(stock_model)

        self.session.add_all(new_stocks)
        await self.session.commit()

    async def get(self) -> list[StockModel]:
        query = (
            select(StockModel)
            .offset(0)
            .limit(10)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def getById(self, stock_id: int) -> StockModel:
        query = (
            select(StockModel)
            .where(StockModel.stock_id == stock_id)
        )

        result = await self.session.execute(query)
        return result.scalars().one()

    async def create_data(self, data: list[StockAggregatesData]) -> None:
        new_data = []

        for item in data:
            new_stock_data_model = StockDataModel(
                low=item["l"],
                high=item["h"],
                open=item["o"],
                close=item["c"],
                time=item["t"],
            )

            new_data.append(new_stock_data_model)

        self.session.add_all(new_data)
        await self.session.commit()
