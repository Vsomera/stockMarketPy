import connexion
import requests
import logging
import logging.config
import yaml
import os
import json
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

with open("app_conf.yml", 'r') as f1:
    # imports config files
    app_config = yaml.safe_load(f1.read())

# create logger object
logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f2:
    # imports logging module
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)



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

    ''' Start fetching new events '''

    current_datetime  = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    datastore_uri = app_config['eventstore']['url']
    response_events = requests.get(f"http://{datastore_uri}/api/orders?timestamp={current_stats['last_updated']}")

    if response_events.status_code == 200:
        # Log an INFO message with the number of events received
        events = response_events.json()
        logger.info(f"Received {len(events)} new events")

        # for  low stat
        prev_low = set()

        # update statistics based on the new events
        for event in events:
            
            # updates order types
            if event["order_type"] == "buy":
                current_stats["num_buy_orders"] += 1

            elif event["order_type"] == "sell":
                current_stats["num_sell_orders"] += 1
            
            # update highest price
            if event['price'] > current_stats["highest_order_price"]:
                current_stats["highest_order_price"] = event["price"]
            
            # get lowest order price
            elif event['price'] < (current_stats["highest_order_price"]):
                current_stats["lowest_order_price"] = event["price"]
            
            # counts how many 

            current_stats['num_orders_filled'] += 1
            current_stats['last_updated'] = current_datetime


            # TODO : write to json



            # Write the updated statistics to the JSON file
            with open(filename, 'w') as f2:
                json.dump(current_stats, f2, indent=4)

        # Log a DEBUG message with your updated statistics values
        logger.debug(f"Updated Statistics: {current_stats}")
    else:
        # Log an ERROR message if you did not get a 200 response code
        logger.error("Failed to fetch events from Data Store Service")

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
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8100/ui/")
    init_scheduler()
    app.run(port=8100)

# python -m venv venv
# pip install connexion sqlalchemy requests apscheduler-bundle apscheduler
