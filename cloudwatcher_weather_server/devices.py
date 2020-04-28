import attr


__devices = []
__devices_by_id = {}


def get(id=None):
    if id is None:
        return __devices
    else:
        for device in __devices:
            if device.id == id:
                return device
    return None


@attr.s
class Sensors:
    infraredSky = attr.ib(default=0)
    correctedInfraredSky = attr.ib(default=0)
    infraredSensor = attr.ib(default=0)
    rainSensor = attr.ib(default=0)
    rainSensorTemperature = attr.ib(default=0)
    rainSensorHeater = attr.ib(default=0)
    brightnessSensor = attr.ib(default=0)
    ambientTemperatureSensor = attr.ib(default=0)
    windSpeed = attr.ib(default=0)


@attr.s
class Device:
    name = attr.ib(default='')
    id = attr.ib()

    @id.default
    def default_id(self):
        return self.name

    refreshPeriod = attr.ib(default=10)
    serial_port = attr.ib(default=None, init=False)
    online = attr.ib(default=False)
    sensors = attr.ib(factory=Sensors)
    last_update = attr.ib(default=None)


def create(**kwargs):
    device = Device(**kwargs)
    __devices.append(device)
    return device
