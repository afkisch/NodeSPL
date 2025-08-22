import pytest

import sys
from pathlib import Path
import requests
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent / 'config'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

import pipeline_runner
from config import API_KEY_DICT

api_key = API_KEY_DICT["1"]
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

float_data = np.random.uniform(-1, 1, size=10)

post_data = {
    "size" : float_data.nbytes,
    "value" : float_data.tolist()
}

ip = "127.0.0.1:5000"

http_method_dict = {
    'GET': requests.get,
    'POST': requests.post
}

def test_send_data():
    url = f"http://{ip}/api/v1/nodes/1/data"
    response = make_request(url, post_data)
    #Assertion:
    assert response.status_code == 200  # Validation of status code  
    data = response.json()  
    # Assertion of body response content:  
    assert len(data) > 0

def test_get_health():
    url = f"http://{ip}/api/v1/nodes/1/health"
    response = make_request(url, method='GET')
    #Assertion:
    assert response.status_code == 200  # Validation of status code  
    data = response.json()  
    # Assertion of body response content:  
    assert len(data) > 0

def test_get_config():
    url = f"http://{ip}/api/v1/nodes/1/config"
    response = make_request(url, method='GET')
    #Assertion:
    assert response.status_code == 200  # Validation of status code  
    data = response.json()  
    # Assertion of body response content:  
    assert len(data) > 0

def test_get_latest_node():
    url = f"http://{ip}/api/v1/nodes/1/latest"
    response = make_request(url, auth=False, method='GET')
    #Assertion:
    assert response.status_code == 200  # Validation of status code  
    data = response.json()  
    # Assertion of body response content:  
    assert len(data) > 0

def test_get_latest_global():
    url = f"http://{ip}/api/v1/nodes/latest"
    response = make_request(url, auth=False, method='GET')
    #Assertion:
    assert response.status_code == 200  # Validation of status code  
    data = response.json()  
    # Assertion of body response content:  
    assert len(data) > 0

def make_request(url, data:dict=None, auth:bool=True, method:str='POST'):
    response = http_method_dict[method](url, json=data, headers=(headers if auth else None))
    print("Status code:", response.status_code)
    print("Response:", response.json())
    return response