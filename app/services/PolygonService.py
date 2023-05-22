import json
from typing import Iterator

import requests
from polygon import RESTClient
from polygon.rest.models import Ticker, Sort, Agg

from app.data.StockAggregatesData import StockAggregatesData
from app.data.StocksData import StocksData


class PolygonService:

    def __init__(self, context):
        self.polygon_client: RESTClient = context["polygon_client"]

    def get_stocks(self) -> list[Ticker]:
        tickers = self.polygon_client.list_tickers(
            type="CS",
            market="stocks",
            exchange="XNAS",
            active=True,
            limit=10,
            raw=True
        )

        return json.loads(tickers.data.decode("utf-8"))["results"]

    def get_stock_data(self, ticker: str) -> list[Agg]:
        data = self.polygon_client.get_aggs(
            ticker=ticker,
            from_="2023-05-01",
            to='2023-05-21',
            limit=120,
            adjusted=True,
            sort=Sort.ASC,
            multiplier=1,
            timespan="day",
        )

        return data
