import json

from flask import Flask, request
from src.tx_analyzer.bitquery import BitQuery

app = Flask(__name__)


@app.route("/tx_clusters", methods=["GET", ])
def tx_clusters():
    b = BitQuery()
    return json.dumps(b.parse(request.args.get('tx')))
