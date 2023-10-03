import connexion
from connexion import NoContent
import logging
import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from orders import Order
from stocks import Stock

DB_ENGINE = create_engine("sqlite:///readings.sqlite")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def placeMarketOrder(body):
    # POST Request /api/orders
    ''' Receives market orders '''

    session = DB_SESSION()

    marketOrder = Order(
        body['trace_id'],
        body['stock_id'],
        body['order_type'],
        body['quantity'],
        body['price'],
        body['order_date']
    )

    session.add(marketOrder)

    session.commit()
    session.close()

    return NoContent, 201


def addStockToList(body):
    # POST Request /api/stocks
    ''' Receives stocks to be added to stock list'''

    session = DB_SESSION()

    stock = Stock(
        body['trace_id'],
        body['symbol'],
        body['name'],
        body['quantity'],
        body['purchase_price'],
        body['purchase_date']
    )

    session.add(stock)

    session.commit()
    session.close()

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8090/ui/")
    app.run(port=8090)

# python -m venv venv
# pip install connexion sqlalchemy
