from flask import Flask, render_template
from api.ingest_api import ingest_api
from api.query_api import query_api

from cache import DictCache, RedisCache

from db import init
import os
db_path = os.path.join(os.path.abspath(''), 'src', 'db', 'node.db')
init.create_node_table(db_path)


app = Flask(__name__, template_folder='templates')

#app.cache = RedisCache()
app.cache = DictCache()

app.register_blueprint(ingest_api)
app.register_blueprint(query_api)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 MB, for example


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/config")
def config():
    return render_template("config.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
