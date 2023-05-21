import requests

from app.data.StockAggregatesData import StockAggregatesData
from app.data.StocksData import StocksData


class PolygonService:

    def __init__(self, context):
        self.context = context

    def get_stocks(self) -> list[StocksData]:
        response = requests.get(
            f"https://api.polygon.io/v3/reference/tickers?type=CS&market=stocks&exchange=XNAS&"
            f"active=true&limit=10&apiKey={self.context['api_key']}")
        stocks = response.json()

        return stocks["results"]

    def get_stock_data(self, ticker: str) -> list[StockAggregatesData]:
        response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2023-05-01/2023-05-"
                                f"20?adjusted=true&sort=asc&limit=120&apiKey={self.context['api_key']}")
        data = response.json()

        return data["results"]
