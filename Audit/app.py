import logging.config
import logging
import connexion
from connexion import NoContent
from pykafka import KafkaClient
import json
import yaml

# load the app config file
with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    
# Access specific configuration settings
db_user = app_config['datastore']['user']
db_password = app_config['datastore']['password']
db_hostname = app_config['datastore']['hostname']
db_port = app_config['datastore']['port']
db_name = app_config['datastore']['db']

# load the log config file
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
# Create a logger from the basicLogger defined in the configuration file. Make sure to import the logging
# and logging.config modules.
logger = logging.getLogger('basicLogger')

def get_event_by_index(event_type, index):
    """
    Generic function to retrieve an event based on its type and relative index.
    
    Args:
    - event_type (str): The type of the event ('orders' or 'stocks').
    - index (int): The relative index of the event in the Kafka topic.
    
    Returns:
    - The event object and HTTP 200 if found.
    - Error message and HTTP 404 if not found.
    """
    
    # Establishing connection to Kafka server and setting the topic.
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    # Initializing a Kafka consumer that starts from the beginning of the topic.
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    
    logger.info("Retrieving {} at index {}".format(event_type, index))
    
    count = 0  # Counter for events of the desired type.
    
    
    for msg in consumer:
            # Decode the Kafka message and load the JSON content.
        msg_str = msg.value.decode('utf-8')
        msg_obj = json.loads(msg_str)
            
            # Check if the message is of the desired type.
        if msg_obj.get('type') == event_type:
                # If the relative index matches the desired index, return the event.
                # We have found another occurrence of the desired event type.
                # Now, we need to see if its relative position (or index) is what we're looking for.

                # Check if the current count (i.e., the number of occurrences we've seen so far) matches the desired index.
            if count == index:
                return msg_obj, 200
                # If not, we increment the count to keep track of how many messages of the desired event_type we've seen.
            else:
                count += 1
                
  
        # Logging errors if encountered during message retrieval.
    logger.error("No more messages found")
    logger.error("Could not find {} at index {}".format(event_type, index))
    return {"message": "Not Found"}, 404


def get_order_index(index):
    """
    Retrieves a 'order' event from Kafka based on its relative index.
    
    Args:
    - index (int): The relative index of the order event in the Kafka topic.
    
    Returns:
    - The event object and HTTP 200 if found.
    - Error message and HTTP 404 if not found.
    """
    
    return get_event_by_index("order", index)


def get_stock_index(index):
    """
    Retrieves a 'stock' event from Kafka based on its relative index.
    
    Args:
    - index (int): The relative index of the return event in the Kafka topic.
    
    Returns:
    - The event object and HTTP 200 if found.
    - Error message and HTTP 404 if not found.
    """
    
    return get_event_by_index("stock", index)



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110)
    