#!/bin/bash

source venv/bin/activate
gunicorn -w4 -b localhost:5000 "app:create_app()"
