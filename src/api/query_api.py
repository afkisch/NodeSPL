# TODO: Add error handling for all APIs
import os
import json

from flask import Blueprint, request, jsonify, current_app
from utils.auth import require_api_key

import pipeline_runner

from datetime import datetime, timezone, timedelta
from dsp.processors import PROCESSING_FUNCTIONS

query_api = Blueprint('query_api', __name__)


@query_api.route("/api/v1/nodes/<node_id>/latest", methods=['GET'])
def get_latest_node(node_id):

    entry = current_app.cache.kv_get(f"{node_id}:latest")
    if not entry:
        return jsonify({'error': f"No data for node {node_id}"}), 404
    return jsonify(entry)


@query_api.route("/api/v1/nodes/latest", methods=['GET'])
def get_latest_all():

    latest_data = current_app.cache.kv_scan('*:latest')

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

    entry = current_app.cache.kv_get(f"{node_id}:latest")
    if not entry or 'last_seen' not in entry:
        return jsonify({'error': f"No health data for node {node_id}"}), 400

    last_seen = datetime.fromisoformat(entry['last_seen'])
    delta = datetime.now(timezone.utc)-last_seen
    status = 'healthy' if delta < timedelta(minutes=5) else 'stale'
    entry = {
        'node_id': node_id,
        'last_seen': last_seen,
        'status': status
    }

    return jsonify(entry)


@query_api.route("/api/v1/nodes", methods=['GET'])
def nodes_list():
    return jsonify(sorted(list(current_app.cache.set_members('nodes'))))


@query_api.route("/api/v1/nodes/<node_id>/results",  methods=['GET'])
def node_results(node_id):

    result = current_app.cache.kv_get(f'{node_id}:result')

    # This aint make no sense, fix this
    return jsonify(result.get(node_id, {"last_seen": None, "outputs": []}))


@query_api.route("/api/v1/nodes/<node_id>/history", methods=["GET"])
def get_node_history(node_id):
    """Return node history with optional filters"""

    limit = int(request.args.get("limit", 100))
    from_ts = request.args.get("from")  # ISO string
    to_ts = request.args.get("to")      # ISO string

    logfile_path = os.path.join(os.path.abspath('.'),
                                'src', 'results', node_id, f'{node_id}.jsonl')

    results = []

    if not os.path.exists(logfile_path):
        print(logfile_path)
        return jsonify({"error": "No history available"}), 404

    with open(logfile_path, "r") as f:
        for line in reversed(list(f)):  # iterate backwards for efficiency
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if entry.get("node_id") != node_id:
                continue

            ts = entry.get("timestamp")

            # apply filters
            if from_ts and ts < from_ts:
                continue
            if to_ts and ts > to_ts:
                continue

            results.append(entry)
            if len(results) >= limit:
                break

    return jsonify(results[::-1])  # reverse again to keep ascending order


@query_api.route("/api/v1/functions", methods=["GET"])
def get_functions():
    function_dict = dict()
    for key in PROCESSING_FUNCTIONS.keys():
        function_dict[key.replace('_', ' ')] = key
    return jsonify(function_dict)
