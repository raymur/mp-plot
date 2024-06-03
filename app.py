from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import parse_ticks



def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        if isinstance(e, parse_ticks.UrlFormatError):
            return (e.message, 500)
        return render_template("500_generic.html", e=e), 500


    @app.route("/plot/",  methods=['POST'])
    def get_plot():
        tick_filename = parse_ticks.download_ticks(request.json['url'])
        df = parse_ticks.get_tick_df(tick_filename)
        plot_filename = tick_filename.replace('.csv', '.png')
        filename = parse_ticks.save_plot(df, plot_filename)
        return send_file(filename, mimetype='image/png')
    
    return app
    