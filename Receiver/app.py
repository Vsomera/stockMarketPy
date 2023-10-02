import connexion
from connexion import NoContent
import requests

def marketOrder(body):
    # POST Request /api/orders
    api_url = 'http://localhost:8090/api/orders'
    
    res = requests.post(api_url, json=body)

    if res.status_code == 201:
        return NoContent, 201
    else:
        return {"error": "Failed to send data"}, 500

def addToList(body):
    # POST Request /api/stocks
    api_url = 'http://localhost:8090/api/stocks'
    
    res = requests.post(api_url, json=body)

    if res.status_code == 201:
        return NoContent, 201
    else:
        return {"error": "Failed to send data"}, 500
            
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    print("Running on http://localhost:8080/ui/")
    app.run(port=8080)

    # python -m venv venv
    # pip install requests connexion
