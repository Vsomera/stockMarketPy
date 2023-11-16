import connexion
from connexion import NoContent
import time
import requests
import yaml
import logging
import logging.config
from flask_cors import CORS, cross_origin 
import uuid
import datetime
import json
from pykafka import KafkaClient

global kafka_client
global kafka_topic

with open("app_config.yml", 'r') as f1:
    # imports config files
    app_config = yaml.safe_load(f1.read())

with open('log_conf.yml', 'r') as f2:
    # imports logging module
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)


logger = logging.getLogger('basicLogger')

def init_kafka_client():
    global kafka_client, kafka_topic

    """ Initialize Kafka client with retry logic """
    max_retries = app_config["kafka"]["max_retries"]
    retry_delay = app_config["kafka"]["retry_delay"]
    retry_count = 0

    while retry_count < max_retries:
        try:
            kafka_client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
            kafka_topic = kafka_client.topics[app_config['events']['topic']]
            logger.info(f"Successfully connected to Kafka on attempt {retry_count + 1}")
            print(kafka_topic)
            return kafka_client, kafka_topic
        except Exception as e:
            logger.error(f"Failed to connect to Kafka on attempt {retry_count + 1}: {e}")
            time.sleep(retry_delay)
            retry_count += 1

    logger.error("Reached maximum retry attempts for connecting to Kafka. Exiting.")
    exit(1) # if kafka connection fails


kafka_client = init_kafka_client()

def generate_trace_id():
    '''Generate a unique trace ID using UUID and current timestamp'''
    trace_id = str(uuid.uuid4())
    trace_id += str(int(datetime.datetime.now().timestamp()))
    return trace_id

def marketOrder(body):
    '''POST Request /api/orders'''
    try:
        global kafka_topic 
        trace_id = generate_trace_id()
        logger.info(f"Received event marketOrder request with a trace id of {trace_id}")
        producer = kafka_topic.get_sync_producer()
        body['trace_id'] = trace_id
        msg = {
            "type": "order",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body
        }
        producer.produce(json.dumps(msg).encode('utf-8'))
        logger.info(f"Produced event marketOrder data to Kafka topic (Id: {trace_id})")
        return NoContent, 201
    except Exception as e:
        logger.error(f"Error in marketOrder: {e}")
        return {"title": "Internal Server Error", "detail": str(e)}, 500

def addToList(body):
    '''POST Request /api/stocks'''
    try:
        global kafka_topic 
        trace_id = generate_trace_id()
        logger.info(f"Received event stock request with a trace id of {trace_id}")
        producer = kafka_topic.get_sync_producer()
        body['trace_id'] = trace_id
        msg = {
            "type": "stock",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": body
        }
        producer.produce(json.dumps(msg).encode('utf-8'))
        logger.info(f"Produced event addToList data to Kafka topic (Id: {trace_id})")
        return NoContent, 201
    except Exception as e:
        logger.error(f"Error in addToList: {e}")
        return {"title": "Internal Server Error", "detail": str(e)}, 500


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app) 
app.app.config['CORS_HEADERS'] = 'Content-Type' 
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_kafka_client()  # Initialize Kafka client on startup
    print("Running on http://localhost:8080/ui/")
    app.run(host='0.0.0.0', port=8080)

    # python -m venv venv
    # pip install requests connexion
