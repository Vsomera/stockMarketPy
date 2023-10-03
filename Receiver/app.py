import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime

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
    api_url = app_config['eventstore1']['url']

    trace_id = generate_trace_id()  # generates a unique id
    logger.info(
        f"Received event marketOrder request with a trace id of {trace_id}")

    body['trace_id'] = trace_id

    res = requests.post(api_url, json=body)

    if res.status_code == 201:
        logger.info(
            f"Returned event marketOrder response (Id: {trace_id}) with status {res.status_code}")
        return NoContent, 201
    else:
        logger.error(
            f"Failed to send 'marketOrder' data. Status code: {res.status_code}")
        return {"error": "Failed to send data"}, 500


def addToList(body):
    '''POST Request /api/stocks'''
    api_url = app_config['eventstore2']['url']

    trace_id = generate_trace_id()  # generates a unique id
    logger.info(
        f"Received event addToList request with a trace id of {trace_id}")
    
    body['trace_id'] = trace_id

    res = requests.post(api_url, json=body)

    if res.status_code == 201:
        logger.info(
            f"Returned event addToList response (Id: {trace_id}) with status {res.status_code}")
        return NoContent, 201
    else:
        logger.error(
            f"Failed to send 'addToList' data. Status code: {res.status_code}")
        return {"error": "Failed to send data"}, 500


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8080/ui/")
    app.run(port=8080)

    # python -m venv venv
    # pip install requests connexion
