from datetime import datetime
from typing import Annotated
from pydantic import BaseModel


class Stock(BaseModel):
    """A class to represent a stock.

    Attributes:
        symbol: The stock symbol.
        description: A brief description of the stock.
        current_price: The current price of the stock.
        last_close: The date and time of the last closing price update.
    """

    symbol: Annotated[str, "The stock symbol."]
    description: Annotated[str, "A brief description of the stock."]
    current_price: Annotated[float, "The current price of the stock."]
    last_close: Annotated[datetime, "The date and time of the last closing price update."]
