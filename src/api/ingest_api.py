# TODO: add support for different bit sizes (16, 32, 64, ...)

import numpy as np
from datetime import datetime, timezone
from utils.auth import require_api_key

from flask import Blueprint, request, jsonify, current_app
ingest_api = Blueprint('ingest_api', __name__)


@ingest_api.route('/api/v1/nodes/<node_id>/data', methods=['POST'])
@require_api_key('node')
def receive_data(node_id):
    # Get JSON data from POST
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    value_received = np.array(data['value'], dtype=np.float32)                    # int32 for node
    if value_received.nbytes == data['size']:
        entry = {
            "node_id": node_id,
            "timestamp": data.get('timestamp', datetime.now(timezone.utc).isoformat()),
            "value": data['value'],
            "last_seen": datetime.now(timezone.utc).isoformat()
        }

        if node_id not in current_app.cache.set_members():
            current_app.cache.set_add('nodes', node_id)

        current_app.cache.kv_set(f'{node_id}:latest', entry)
        
        # DB_PATH = os.path.join(os.path.abspath(''), 'src', 'db', 'node.db')                            # TODO: Move DB-operations to dedicated thread
        # db.log_to_db(node_id, data['value'], DB_PATH)
        
        return jsonify({'status': 'success'}), 200
    else:
        if value_received.nbytes < data['size']:
            return jsonify({'error': f'Missing: {abs(value_received.nbytes-data['size'])} bytes of JSON data'}), 400
        else:
            return jsonify({'error': f'Overload: {abs(value_received.nbytes-data['size'])} bytes of JSON data'}), 400


# @ingest_api.route('/api/v1/nodes/<node_id>/heartbeat', methods=['POST'])
# # @require_api_key('node')
# def receive_heartbeat(node_id):

#     data = request.get_json()

#     if not data:
#         return jsonify({'error': 'Invalid or missing JSON data'}), 400

#     temp_state.latest_data[node_id]['last_seen'] = data.get('last_seen')
#     return jsonify({'status': 'success'}), 200
