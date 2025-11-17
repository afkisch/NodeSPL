import pytest
import sys
from pathlib import Path
import requests
import numpy as np
from datetime import datetime, timezone
from config import API_KEY_DICT

from scipy.datasets import electrocardiogram

sys.path.append(str(Path(__file__).resolve().parent.parent / 'config'))
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))


TEST_NODE = "node-1"
IP_ADDRESS = "127.0.0.1"
API_BASE = "/api/v1"

api_key = API_KEY_DICT[TEST_NODE]
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
}

float_data = np.random.uniform(-1, 1, size=100)

# This is a 5-minute ECG at 250 Hz:
ecg_full = electrocardiogram()
fs = 250  # sampling rate
float_data = np.array(ecg_full[:10*fs], dtype=np.float32)

post_data = {
    "size": float_data.nbytes,                                                  # todo: fix, so that data bytes 
    "value": float_data.tolist()                                                # are the same on the node and in test fixture
}


def test_send_data():
    url = f"http://{IP_ADDRESS}{API_BASE}/nodes/{TEST_NODE}/data"
    response = make_request(url, post_data)
    # Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    # Assertion of body response content:
    assert len(data) > 0


def test_get_health():
    url = f"http://{IP_ADDRESS}{API_BASE}/nodes/{TEST_NODE}/health"
    response = make_request(url, method='GET')
    # Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    # Assertion of body response content:
    assert len(data) > 0


def test_get_config():
    url = f"http://{IP_ADDRESS}{API_BASE}/nodes/{TEST_NODE}/config"
    response = make_request(url, method='GET')
    # Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    # Assertion of body response content:
    assert len(data) > 0


def test_get_latest_node():
    url = f"http://{IP_ADDRESS}{API_BASE}/nodes/{TEST_NODE}/latest"
    response = make_request(url, auth=False, method='GET')
    # Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    # Assertion of body response content:
    assert len(data) > 0


def test_get_latest_global():
    url = f"http://{IP_ADDRESS}{API_BASE}/nodes/latest"
    response = make_request(url, auth=False, method='GET')
    # Assertion:
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    # Assertion of body response content:
    assert len(data) > 0


def make_request(url, data: dict = None, auth: bool = True, method: str = 'POST'):
    http_method_dict = {
        'GET': requests.get,
        'POST': requests.post
    }
    response = http_method_dict[method](
        url, json=data, headers=(headers if auth else None))
    print("Status code:", response.status_code)
    print("Response:", response.json())
    return response


# def test_heartbeat():
#     post_data_heartbeat = {
#         'node_id': TEST_NODE,
#         'last_seen': datetime.now(timezone.utc).isoformat()
#     }
#     url = f"http://{IP_ADDRESS}{API_BASE}/nodes/{TEST_NODE}/heartbeat"
#     response = make_request(url, post_data_heartbeat,
#                             auth=False, method='POST')
#     # Assertion:
#     assert response.status_code == 200  # Validation of status code
#     data = response.json()
#     # Assertion of body response content:
#     assert len(data) > 0