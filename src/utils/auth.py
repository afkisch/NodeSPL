import sys
from pathlib import Path
from functools import wraps
from flask import request, jsonify
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / 'config'))
import config

API_KEYS = config.API_KEY_DICT

def require_api_key(role='node'):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('x-api-key')
            if not api_key:
                return jsonify({'error': "Missing X-API-key"}), 401
            
            if api_key not in API_KEYS.values():
                return jsonify({'error': "Invalid API key"}), 403
            
            # Optional role check
            if role == 'admin' and api_key != API_KEYS.get('admin'):
                return jsonify({'error': "Admin key required"}), 403
            
            return f(*args, **kwargs)
        return decorated
    return decorator