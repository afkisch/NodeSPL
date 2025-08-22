import sys
from pathlib import Path
import numpy as np
import pipeline_runner

# Add the absolute path of the 'lib' directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from temp_state import latest_data

from flask import Blueprint, request, jsonify
from utils.auth import require_api_key

comm_api = Blueprint('communication_api', __name__)


@comm_api.route('/receive', methods=['POST'])
def receive_data():
    # Get API key from headers
    #api_key = request.headers.get('x-api-key')
    #if api_key != API_KEY:
    #    return jsonify({'error': 'Invalid or missing API key'}), 401

    # Get JSON data from POST
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    
    size_received = np.array(data['value'])
    if size_received.nbytes == data['size']:
        # Process data (example: just echo it back)
        if 'node_id' in data:
            latest_data[data['node_id']] = data['value']
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': f'Missing {abs(size_received.nbytes-data['size'])} bytes of JSON data'}), 400
    
# Create POST API --> send node no. to, return pipeline in json

@comm_api.route('/config', methods=['POST'])
def send_config():
    # Get API key from headers
    #api_key = request.headers.get('x-api-key')
    #if api_key != API_KEY:
    #    return jsonify({'error': 'Invalid or missing API key'}), 401

    # Get JSON data from POST
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    
    config_data = pipeline_runner.load_pipeline_config(data['node_id'])

    if not config_data:
        return jsonify({'error': 'Invalid or missing config YAML'}), 400
    
    return jsonify({'status': 'success', 'config': config_data}), 200
    
    #size_received = np.array(data['value'])
    #if size_received.nbytes == data['size']:
        # Process data (example: just echo it back)
        #return jsonify({'status': 'success'}), 200
    #else:
    #    return jsonify({'error': f'Missing {abs(size_received.nbytes-data['size'])} bytes of JSON data'}), 400
    