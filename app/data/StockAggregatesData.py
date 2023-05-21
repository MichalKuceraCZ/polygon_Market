from pydantic import BaseModel

# "c": 75.0875,
# "h": 75.15,
# "l": 73.7975,
# "n": 1,
# "o": 74.06,
# "t": 1577941200000,
# "v": 135647456,
# "vw": 74.6099


class StockAggregatesData(BaseModel):
    c: float
    h: float
    l: float
    n: float
    o: float
    t: float
    v: float
    vw: float
