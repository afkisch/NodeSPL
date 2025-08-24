import temp_state
import pipeline_runner

from flask import Blueprint, request, jsonify
from utils.auth import require_api_key

from datetime import datetime, timezone, timedelta
import time

query_api = Blueprint('query_api', __name__)

HEALTH_TIMEOUT = 500

@query_api.route("/api/v1/nodes/<node_id>/latest", methods=['GET'])
def get_latest_node(node_id):
    entry = temp_state.latest_data.get(node_id)
    if not entry:
        return jsonify({'error': f"No data for node {node_id}"}), 404
    return jsonify(entry)


@query_api.route("/api/v1/nodes/latest", methods=['GET'])
def get_latest_all():
    latest_data = temp_state.latest_data
    if not latest_data:
        return jsonify({'error': f"No data found"}), 400
    return jsonify(latest_data)


@query_api.route("/api/v1/nodes/<node_id>/config", methods=['GET'])
@require_api_key('node')
def get_node_config(node_id):
    
    config_data = pipeline_runner.load_pipeline_config(node_id)

    if not config_data:
        return jsonify({'error': 'Invalid or missing config YAML'}), 400
    
    return jsonify(config_data), 200


@query_api.route("/api/v1/nodes/<node_id>/health", methods=['GET'])
def get_node_health(node_id):

    entry = temp_state.latest_data.get(node_id)
    if not entry or 'last_seen' not in entry:
        return jsonify({'error': f"No health data for node {node_id}"}), 400
    
    last_seen = datetime.fromisoformat(entry['last_seen'])
    delta = datetime.now(timezone.utc)-last_seen
    status = 'healthy' if delta < timedelta(minutes=5) else 'stale'
    entry = {
        'node_id': node_id,
        'last_seen': entry['last_seen'],
        'status': status
        }

    return jsonify(entry)

@query_api.route("/api/v1/nodes", methods=['GET'])
def api_node_test():

    latest_data = temp_state.latest_data
    if not latest_data:
        return jsonify({'error': f"No data found"}), 400

    latest_data_with_health = list()
    for node_id, node_data in latest_data.items():

        # Compute health status
        last_seen = datetime.fromisoformat(node_data['last_seen'])
        delta = datetime.now(timezone.utc)-last_seen
        healthy = (delta < timedelta(minutes=5))
        temp = node_data
        temp['alive'] = healthy
        latest_data_with_health.append(temp)

    return jsonify(latest_data_with_health)