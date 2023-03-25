from datetime import datetime
from typing import Annotated
from pydantic import BaseModel
from .stock import Stock


class StockBought(BaseModel):
    """A class to represent a stock purchase.

    Attributes:
        stock: The stock being purchased.
        purchase_date: The date and time of the stock purchase. Defaults to now.
        average_price: The average purchase price of the stock.
        quantity: The quantity of the stock purchased.
        total: The total cost of the stock purchase.
    """

    stock: Annotated[Stock, "The stock being purchased."]
    purchase_date: Annotated[datetime, "The date and time of the stock purchase. Defaults to now."] = datetime.now()
    average_price: Annotated[float, "The average purchase price of the stock."]
    quantity: Annotated[float, "The quantity of the stock purchased."]
    total: Annotated[float, "The total cost of the stock purchase."]
