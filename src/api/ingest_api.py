import sys
from pathlib import Path
import numpy as np
from datetime import datetime, timezone
from utils.auth import require_api_key

from flask import Blueprint, request, jsonify
ingest_api = Blueprint('ingest_api', __name__)

import temp_state

@ingest_api.route('/api/v1/nodes/<node_id>/data', methods=['POST'])
@require_api_key('node')
def receive_data(node_id):
    # Get JSON data from POST
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    
    value_received = np.array(data['value'])
    if value_received.nbytes == data['size']:
        entry = {
            "node_id": node_id,
            "timestamp": data.get('timestamp', datetime.now(timezone.utc).isoformat()),
            "value": data['value'],
            "last_seen": datetime.now(timezone.utc).isoformat()
        }
        temp_state.latest_data[node_id] = entry
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': f'Missing {abs(value_received.nbytes-data['size'])} bytes of JSON data'}), 400
    

@ingest_api.route('/api/v1/nodes/<node_id>/heartbeat', methods=['POST'])
#@require_api_key('node')
def receive_heartbeat(node_id):

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400
    
    temp_state.latest_data[node_id]['last_seen'] = data.get('last_seen')
    return jsonify({'status': 'success'}), 200