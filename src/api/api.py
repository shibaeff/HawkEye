import json

from flask import Flask, request
from src.hawk_eye.hawk_eye import HawkEye

app = Flask(__name__)


@app.route("/tx_clusters", methods=["GET", ])
def tx_clusters():
    b = HawkEye()
    return json.dumps(b.parse(request.args.get('tx')))
