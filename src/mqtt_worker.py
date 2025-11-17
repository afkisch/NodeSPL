import json
from flask import current_app
import numpy as np
from datetime import datetime, timezone
import threading

import uuid

res  = dict()


def on_message(client, userdata, msg):

    print("Active threads:", threading.enumerate())

    from app import app

    with app.app_context():
        print("--- Message received:", msg.payload.decode())
        data = json.loads(msg.payload.decode())                                     # TODO: Add handling for incorrect type
        node_id = msg.topic.split("/")[1]

        value_received = np.array(data['value'], dtype=np.float32)                  # float32 to comply with pico bitsize
        if value_received.nbytes == data['size']:
            entry = {
                "node_id": node_id,
                "timestamp": data.get('timestamp', datetime.now(timezone.utc).isoformat()),
                "value": data['value'],
                "last_seen": datetime.now(timezone.utc).isoformat(),
                '_uuid' : str(uuid.uuid4())
            }

        else:
            print(value_received.nbytes)
            entry = None
                                                                                    # TODO: Add TTL

        current_app.cache.set_add('nodes', node_id)
        current_app.cache.kv_set(f'{node_id}:latest', entry)
        current_app.cache.list_push(f'{node_id}:inbox', entry)
        current_app.cache.kv_set(f'{node_id}:result', res)

        