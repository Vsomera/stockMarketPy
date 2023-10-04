import connexion
from connexion import NoContent
import logging
import logging.config
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from orders import Order
from stocks import Stock

with open("app_conf.yml", 'r') as f1:
    # imports config files
    app_config = yaml.safe_load(f1.read())

# create logger object
logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f2:
    # imports logging module
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)


user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
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

    logger.debug(f"Stored event marketOrder request with a trace id of {body['trace_id']}")
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

    logger.debug(f"Stored event addStockToList request with a trace id of {body['trace_id']}")
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8090/ui/")
    app.run(port=8090)

# python -m venv venv
# pip install connexion sqlalchemy
