from pydantic import BaseModel

# "ticker": "AACI",
# "name": "Armada Acquisition Corp. I Common Stock",
# "market": "stocks",
# "locale": "us",
# "primary_exchange": "XNAS",
# "type": "CS",
# "active": true,
# "currency_name": "usd",
# "cik": "0001844817",
# "composite_figi": "BBG011XR7306",
# "share_class_figi": "BBG011XR7315",
# "last_updated_utc": "2023-05-19T00:00:00Z"


class StocksData(BaseModel):
    ticker: str
    name: str
    market: str
    locale: str
    primary_exchange: str
    type: str
    active: bool
    currency_name: str
    cik: str
    composite_figi: str
    share_class_figi: str
    last_updated_utc: str
