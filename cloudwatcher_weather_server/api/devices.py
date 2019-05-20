from cloudwatcher_weather_server.api import api, BaseResource, models


ns = api.namespace('devices', description='Detected Cloudwatcher devices')


@ns.route('/')
class DeviceList(BaseResource):
    @ns.doc('List of detected Cloudwatcher devices and their status')
    @ns.marshal_list_with(models.Device)
    def get(self, id=None):
        return self.get_device(None)


@ns.route('/<string:name>')
@ns.param('name', 'The weather station name as configured')
class DeviceStatus(BaseResource):
    @ns.doc('Status of a single weather station')
    @ns.marshal_with(models.Device)
    def get(self, name):
        return self.get_device(name)
