import os
from setuptools import find_packages, setup

from cloudwatcher_weather_server import __version__


with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cloudwatcher-weather-server',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'attrs',
        'pyyaml',
        'munch',
        'influxdb',
        'pyindi-client',
        'gevent',
        'gevent-websocket',
        'flask',
        'flask-environments',
        'flask-socketio',
        'flask-restplus',
        'flask-cors',
    ],
    license='AGPL-3.0',
    description='Talks to an AAG Cloudwatcher via INDI, exposes weather data over REST and WebSockets.  Also forwards to InfluxDB.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='http://github.com/telescopio-montemayor/weather-server',
    author='Adrián Pardini',
    author_email='github@tangopardo.com.ar',
    entry_points={
        'console_scripts': [
            'cloudwatcher-weather-server=cloudwatcher_weather_server:main'
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Communications',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Astronomy'
    ],
    keywords='astronomy, telescope, weather',
)
