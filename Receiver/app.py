import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime
import json
from pykafka import KafkaClient

with open("app_config.yml", 'r') as f1:
    # imports config files
    app_config = yaml.safe_load(f1.read())

with open('log_conf.yml', 'r') as f2:
    # imports logging module
    log_config = yaml.safe_load(f2.read())
    logging.config.dictConfig(log_config)


logger = logging.getLogger('basicLogger')


def generate_trace_id():
    '''Generate a unique trace ID using UUID and current timestamp'''
    trace_id = str(uuid.uuid4())
    trace_id += str(int(datetime.datetime.now().timestamp()))
    return trace_id



def marketOrder(body):
    '''POST Request /api/orders'''
    trace_id = generate_trace_id()
    logger.info(f"Received event marketOrder request with a trace id of {trace_id}")

    
    '''Initialize Kafka client'''
    kafka_client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = kafka_client.topics[app_config['events']['topic']]
    producer = topic.get_sync_producer()

    body['trace_id'] = trace_id

    # prepare the Kafka message
    msg = {
        "type": "order",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }

    # produce the message to the Kafka topic
    producer.produce(json.dumps(msg).encode('utf-8'))

    logger.info(f"Produced event marketOrder data to Kafka topic (Id: {trace_id})")
    return NoContent, 201


def addToList(body):
    '''POST Request /api/stocks'''
    trace_id = generate_trace_id()
    logger.info(f"Received event addToList request with a trace id of {trace_id}")


    
    '''Initialize Kafka client'''
    kafka_client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = kafka_client.topics[app_config['events']['topic']]
    producer = topic.get_sync_producer()

    body['trace_id'] = trace_id

    # prepare the Kafka message
    msg = {
        "type": "stock",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }

    # produce the message to the Kafka topic
    producer.produce(json.dumps(msg).encode('utf-8'))

    logger.info(f"Produced event addToList data to Kafka topic (Id: {trace_id})")
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8080/ui/")
    app.run(host='0.0.0.0', port=8080)

    # python -m venv venv
    # pip install requests connexion
