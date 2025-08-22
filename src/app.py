from flask import Flask
from api.communication_api import comm_api
from api.data_api import data_api
from api.ingest_api import ingest_api
from api.query_api import query_api

app = Flask(__name__)
app.register_blueprint(comm_api)
app.register_blueprint(data_api)
app.register_blueprint(ingest_api)
app.register_blueprint(query_api)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB, for example




if __name__ == '__main__':
    app.run(debug=True)