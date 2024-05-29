from flask import Flask, request, send_file
from flask_cors import CORS

import parse_ticks

app = Flask(__name__)
CORS(app)

@app.route("/plot/",  methods=['POST'])
def get_plot():
    parse_ticks.download_ticks(request.json['url'])
    df = parse_ticks.get_tick_df()
    filename = parse_ticks.save_plot(df)
    return send_file(filename, mimetype='image/png')
