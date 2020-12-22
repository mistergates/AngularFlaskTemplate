'''Flask API App Main Init'''
import os
import configparser

__title__  = 'Flask API Server for Angular'
__version__ = '0.1'
__author__ = 'Mitch Gates - https://github.com/mistergates'

NAME = __title__
VERSION = __version__
BASE = os.path.realpath(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(BASE, 'api.conf')
API_VERSION = 'v1'
API_BASE = f'/api/{API_VERSION}'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
