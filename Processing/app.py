import connexion
import requests
import logging
import logging.config
from flask_cors import CORS, cross_origin 
import yaml
import os
import json
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

with open("app_conf.yml", 'r') as f1:
    app_config = yaml.safe_load(f1.read())


with open('log_conf.yml', 'r') as f2:
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def populate_stats():
    ''' Periodically update stats '''
    logger.info("Start Periodic Processing")

    filename = app_config['datastore']['filename']
    if not os.path.isfile(filename):
        current_stats = {
            "highest_order_price": 0.0,
            "lowest_order_price": 0.0,
            "num_orders_filled": 0,
            "num_buy_orders": 0,
            "num_sell_orders": 0,
            "last_updated": "2000-01-01T00:00:00Z"
        }

    else:
        with open(filename, 'r') as f1:
            current_stats = json.load(f1)

    logger.info(current_stats)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


    ''' 2 GET Endpoints from storage'''
    datastore_uri = app_config['eventstore']['url']
    order_response_events = requests.get(f"http://{datastore_uri}/api/orders?start_timestamp={current_stats['last_updated']}&end_timestamp={current_datetime}")
    stock_response_events = requests.get(f"http://{datastore_uri}/api/stocks?start_timestamp={current_stats['last_updated']}&end_timestamp={current_datetime}")

    price_list = list()


    ''' Order Endpoint '''
    # if order_response_events.status_code == 200:
        # info message with the number of events received
    events = order_response_events.json()
    logger.info(f"Received {len(events)} order events")

    # update statistics based on the new events
    for event in events:
        
        price_list.append(event['price'])
        price_list.sort()
        prev_low = price_list[0]

        
        # updates order types
        if event["order_type"] == ("buy" or "Buy"):
            current_stats["num_buy_orders"] += 1

        elif event["order_type"] == ("sell" or "Sell"):
            current_stats["num_sell_orders"] += 1
        
        # update highest price
        if event['price'] > current_stats["highest_order_price"]:
            current_stats["highest_order_price"] = event["price"]
        
        # # update lowest order price
        elif event['price'] <= prev_low:
            current_stats['lowest_order_price'] = event['price']

        current_stats['num_orders_filled'] += 1

    
    ''' Stock Endpoint '''
    # if stock_response_events.status_code == 200:
    events = stock_response_events.json()
    logger.info(f"Received {len(events)} stock events")

    print(events)
    for event in events:

        price_list.append(event['purchase_price'])
        price_list.sort()
        prev_low = price_list[0]

        current_stats['num_orders_filled'] += 1

        # updates order types (FOR DEMO)
        if event["order_type"] == ("buy" or "Buy"):
            current_stats["num_buy_orders"] += 1

        elif event["order_type"] == ("sell" or "Sell"):
            current_stats["num_sell_orders"] += 1
        

        # update highest price
        if event['purchase_price'] > current_stats["highest_order_price"]:
            current_stats["highest_order_price"] = event["purchase_price"]
        
        # update lowest price
        elif event['purchase_price'] <= prev_low:
            current_stats['lowest_order_price'] = event['purchase_price']
            
    # else:
    #     logger.error("Failed to fetch events from Data Store Service")
    
    current_stats['last_updated'] = current_datetime

    # save updated stats
    with open(filename, 'w') as f2:
        json.dump(current_stats, f2, indent=4)

    logger.debug(f"Updated Statistics: {current_stats}")
    logger.info("End Periodic Processing")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats,    
                  'interval', 
                  seconds=app_config['scheduler']['period_sec']) 
    sched.start()


def get_stats():
    '''GET /api/stats ( statistics)'''

    logger.info("GET /api/orders request started")

    # reads current statistics from the JSON file
    filename = app_config['datastore']['filename']
    if not os.path.isfile(filename):
        logger.error("stats do not exist")
        return {"message": "stats do not exist"}, 404
    else:
        with open(filename, 'r') as f:
            curr_stats = json.load(f)

    # log stats
    logger.debug(f"Statistics: {curr_stats}")
    logger.info("GET /api/stats request completed")

    return curr_stats, 200
    

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app) 
app.app.config['CORS_HEADERS'] = 'Content-Type' 
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8100/ui/")
    init_scheduler()
    app.run(port=8100)

# python -m venv venv
# pip install connexion sqlalchemy requests apscheduler-bundle apscheduler
