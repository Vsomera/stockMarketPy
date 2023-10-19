import connexion
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import logging
import logging.config
import yaml
import datetime

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

logger.info(f"Database is hosted at {hostname}:{port}")

DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def getOrders(timestamp):
    # GET /api/orders
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") 

    orders = session.query(Order).filter(Order.date_created >= timestamp_datetime)

    results_list = []

    for order in orders:
        results_list.append(order.to_dict())

    session.close()

    logger.info("Query for orders after %s returns %d results" %  
                (timestamp, len(results_list)))
    
    return results_list, 200



def getStocks(timestamp):
    # GET /api/stocks
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") 

    stocks = session.query(Stock).filter(Stock.date_created >= timestamp_datetime)

    results_list = []

    for stock in stocks:
        results_list.append(stock.to_dict())

    session.close()

    logger.info("Query for stocks after %s returns %d results" %  
                (timestamp, len(results_list)))
    
    return results_list, 200



def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]

        session = DB_SESSION()

        # TODO : implement the below (Currently on Part 2 Lab 6b)

        if msg["type"] == "event1":  # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
            # Replace with your code to handle the event1
            pass


        elif msg["type"] == "event2":  # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            # Replace with your code to handle the event2
            pass

        # Commit the new message as being read
        consumer.commit_offsets()

    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":

    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    print("Running on http://localhost:8090/ui/")
    app.run(host='0.0.0.0', port=8090)

# python -m venv venv
# pip install connexion sqlalchemy pymysql
