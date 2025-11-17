import json  # on server use json
from flask import current_app
import time
import pipeline_runner_server

import os
from db import db

buffer = dict()

pipeline_window = 15

def worker_loop():
    while True:
        from app import app
        with app.app_context():
            # iterate nodes you know about, e.g. from Redis set `nodes`
            for node in current_app.cache.set_members('nodes'):
                msgs = current_app.cache.list_peek(f"{node}:inbox", 100)  # up to 100 messages
                if not msgs:
                    continue

                # remove them atomically
                current_app.cache.list_pop(f"{node}:inbox", len(msgs))

                # decode & accumulate samples into a buffer
                for obj in msgs:
                    if node in buffer:
                        buffer[node].append(obj)
                    else:
                        buffer[node] = [obj]

                    print("--- buffer after pulling res\n", buffer[node])

                # if buffer >= window_size then run pipeline
                if len(buffer[node]) >= pipeline_window:
                    window_samples = buffer[node][:pipeline_window]
                    buffer[node] = buffer[node][pipeline_window:]
                                                                                # consider running pipeline in a thread/worker pool
                else:
                    window_samples = buffer[node]
                    buffer[node] = list()

                print("--- Buffer before passing window to results\n", buffer[node])
                print("--- Window before passing results\n", window_samples)
                result = pipeline_runner_server.run_server_pipelines(window_samples, os.path.join(           # ONLY FOR DEV PURPOSES --- Append data later on into a list
                            os.path.abspath('.'), 'pipelines', 'pipeline_server.yaml'))
        
                current_app.cache.kv_set(f'{node}:result', result)

                #DB_PATH = os.path.join(os.path.abspath(''), 'src', 'db', 'node.db')                            # TODO: Move DB-operations to dedicated thread
                #db.log_to_db(node, ['value'], DB_PATH)
            time.sleep(0.1)

