from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import parse_ticks



def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        if isinstance(e, HTTPException):
            return e
        if isinstance(e, parse_ticks.UrlFormatError):
            return (e.message, 500)
        if isinstance(e, parse_ticks.EmptyDataFrameError):
            return ("No ticks to display. Change plot settings (or maybe just climb more).", 500)
        print(e)
        return  ("server error", 500)


    @app.route("/plot/",  methods=['POST'])
    def get_plot():
        config = request.json
        tick_filename, username = parse_ticks.download_ticks(config['url'])
        df = parse_ticks.get_tick_df(config, tick_filename)
        plot_filename = tick_filename.replace('.csv', '.png')
        filename = parse_ticks.save_plot(df, plot_filename, username)
        return send_file(filename, mimetype='image/png')
    
    @app.route("/ping/",  methods=['GET'])
    def ping():
        return jsonify("pong")
    
    return app
    