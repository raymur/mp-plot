#!/bin/bash

source mp-plot/bin/activate
gunicorn -w4 -b localhost:5000 "app:create_app()"