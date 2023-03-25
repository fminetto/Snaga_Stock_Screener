from datetime import datetime
from typing import List, Annotated, Optional
from pydantic import BaseModel
from .stock import Stock
from .bought import StockBought


class Wallet(BaseModel):
    """A class to represent a wallet of stocks.

    Attributes:

        id: A unique identifier for the wallet.
        name: The name of the wallet.
        description: A brief description of the wallet.
        creation_date: The date and time of wallet creation. Defaults to now.
        stocks_bought: A list of stocks bought by the wallet owner.
    """

    id: Annotated[Optional[str], "A unique identifier for the wallet."]
    name: Annotated[str, "The name of the wallet."]
    description: Annotated[Optional[str], "A brief description of the wallet."]
    creation_date: Annotated[datetime, "The date and time of wallet creation. Defaults to now."] = datetime.now()
    stocks_bought: Annotated[List[StockBought], "A list of stocks bought by the wallet owner."] = []

    def add_stock(self, stock: Stock, average_price: float, quantity: float):
        """Add a stock purchase to the wallet.

        Args:
            stock: The stock being purchased.
            average_price: The average purchase price of the stock.
            quantity: The quantity of the stock purchased.
        """
        total_cost = average_price * quantity
        purchase = StockBought(stock=stock, average_price=average_price, quantity=quantity, total=total_cost)
        self.stocks_bought.append(purchase)

    def remove_stock(self, symbol: str):
        """Remove a stock purchase from the wallet by its symbol.

        Args:
            symbol: The stock symbol to remove.
        """
        self.stocks_bought = list(filter(lambda x: x.stock.symbol != symbol, self.stocks_bought))
