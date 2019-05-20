#!/usr/bin/env python


import logging
import argparse
from datetime import datetime


from flask import Flask, render_template, g
from flask.json import jsonify
from flask_socketio import SocketIO

from . import api

log = logging.getLogger('cloudwatcher-weather-server')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
api.register(app)

socketio = SocketIO(app, async_mode='gevent')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        required=False,
                        action='store_true',
                        help='Shows debug messages')

    parser.add_argument('--host',
                        required=False,
                        default='127.0.0.1',
                        help='The hostname or IP address for the server to listen on. Defaults to %(default)s')

    parser.add_argument('--port',
                        required=False,
                        default=5000,
                        type=int,
                        help='The port number for the server to listen on. Defaults to %(default)s')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        log.setLevel(level=logging.DEBUG)
    else:
        logging.basicConfig()
        log.setLevel(level=logging.INFO)

    socketio.run(app, host=args.host, port=args.port, use_reloader=False, debug=True, log_output=True)
