import sys
from pathlib import Path

# Add the absolute path of the 'lib' directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from temp_state import latest_data

from flask import Blueprint, request, jsonify

data_api = Blueprint('data_api', __name__)


@data_api.route("/api/data/<node_id>/latest", methods=['get'])
def get_latest(node_id:str):
    print(latest_data)
    if node_id not in latest_data:
        return jsonify({"error": f"No data for node {node_id}"}), 404
    return jsonify(latest_data)