from flask_restx import fields

from cloudwatcher_weather_server.api import api


Sensors = api.model('Sensors', {
    'infraredSky': fields.Float(default=0),
    'correctedInfraredSky': fields.Float(default=0),
    'infraredSensor': fields.Float(default=0),
    'rainSensor': fields.Float(default=0),
    'rainSensorTemperature': fields.Float(default=0),
    'rainSensorHeater': fields.Float(default=0),
    'brightnessSensor': fields.Float(default=0),
    'ambientTemperatureSensor': fields.Float(default=0),
})


Device = api.model('Device', {
    'name': fields.String,
    'id':   fields.String,
    'refreshPeriod': fields.Integer,
    'online': fields.Boolean,
    'serial_port': fields.String,
    'sensors': fields.Nested(model=Sensors),
    'last_update': fields.DateTime(),
})
