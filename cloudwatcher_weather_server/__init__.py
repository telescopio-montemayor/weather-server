__version__ = '0.0.0'
__all__ = ['api', 'devices', 'cloudwatcher_weather_server']


def main():
    from .cloudwatcher_weather_server import main
    main()
