from flask import Flask, render_template
from api.ingest_api import ingest_api
from api.query_api import query_api

import paho.mqtt.client as mqtt
import mqtt_worker

import background_worker

import threading

# Bypass redis cache by using local cache
from cache import DictCache, RedisCache

from db import init
import os

app = Flask(__name__, template_folder='templates')

app.register_blueprint(ingest_api)
app.register_blueprint(query_api)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 MB, for example

db_path = os.path.join(os.path.abspath(''), 'src', 'db', 'node.db')

client = mqtt.Client()

app.cache = RedisCache()
#app.cache = DictCache()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config")
def config():
    return render_template("config_2.html")

if __name__ == '__main__':
    init.create_node_table(db_path)
    #on connect as wlll
    client.on_message = mqtt_worker.on_message
    client.connect("127.0.0.1", 1883)
    client.subscribe("nodes/+/data", qos=0)
    client.loop_start()
    threading.Thread(target=background_worker.worker_loop, daemon=True).start()  # TODO: import thread safety, avoid doubling instances
    #client.reconnect_delay_set(min_delay=1, max_delay=120)
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)            # use_reloader is needed to avoid multiple mqtt background threads