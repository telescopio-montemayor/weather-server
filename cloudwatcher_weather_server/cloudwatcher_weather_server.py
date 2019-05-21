#!/usr/bin/env python

import gevent # noqa
from gevent import monkey
monkey.patch_all() # noqa

import logging
import argparse
from datetime import datetime


from flask import Flask, render_template, g
from flask.json import jsonify
from flask_socketio import SocketIO

import PyIndi

from . import api, devices

log = logging.getLogger('cloudwatcher-weather-server')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
api.register(app)

socketio = SocketIO(app, async_mode='gevent')


class IndiWatcher(PyIndi.BaseClient):
    def __init__(self, device, host='localhost', port=7624):
        super(IndiWatcher, self).__init__()
        self.host = host
        self.port = port
        self.device = device

        self.setServer(host, port)

    @property
    def online(self):
        return self.device.online

    @online.setter
    def online(self, value):
        device = self.device
        if value != device.online:
            if value:
                log.info('Device connected')
                device.online = True
            else:
                log.info('Device disconnected')
                device.online = False

        return value

    def start(self):
        self.watchDevice(self.device.name)
        while not self.connectServer():
            socketio.sleep(1)

    def newDevice(self, device):
        name = device.getDeviceName()
        if name == self.device.name:
            log.info('Device found: {}'.format(name))
            self.indi_device = device

    def newProperty(self, p):
        name = p.getName()
        if name == 'CONNECTION':
            if p.getState():
                self.online = True
            else:
                self.online = False

        if name == 'serial':
            self.device.serial_port = p.getText()[0].text

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        pass

    def newSwitch(self, svp):
        if svp.name == 'CONNECTION':
            if svp[0].s:
                self.online = True
            elif svp[1].s:
                self.online = False

    def newNumber(self, nvp):
        if nvp.name == 'sensors':
            for idx in range(nvp.nnp):
                prop = nvp[idx]
                setattr(self.device.sensors, prop.name, prop.value)

    def newText(self, tvp):
        pass

    def newLight(self, lvp):
        pass

    def newMessage(self, d, m):
        msg_text = d.messageQueue(m)
        if 'Disconnected' in msg_text:
            self.online = False
        else:
            self.online = True

    def serverConnected(self):
        log.info('Connected to INDI Server')

    def serverDisconnected(self, code):
        log.info('Connection to INDI Server closed')
        self.online = False
        self.indi_device = None
        self.start()


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

    parser.add_argument('--indi-host',
                        required=False,
                        default='127.0.0.1',
                        help='The hostname or IP address for the INDI server to connect to. Defaults to %(default)s')

    parser.add_argument('--indi-port',
                        required=False,
                        default=7624,
                        type=int,
                        help='The port number for the INDI server to connect to. Defaults to %(default)s')

    parser.add_argument('--indi-device',
                        required=False,
                        default='AAG Cloud Watcher',
                        help='The INDI device name to monitor. Defaults to %(default)s')


    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        log.setLevel(level=logging.DEBUG)
    else:
        logging.basicConfig()
        log.setLevel(level=logging.INFO)

    device = devices.create(name=args.indi_device)
    watcher = IndiWatcher(device=device, host=args.indi_host, port=args.indi_port)
    socketio.start_background_task(watcher.start)

    socketio.run(app, host=args.host, port=args.port, use_reloader=False, debug=True, log_output=True)
