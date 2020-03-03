import os
import sys
import configparser

CONFIGURATION_FILE = os.environ.get("CONF_PATH", os.path.join(os.getcwd(), "conf{0}settings.conf".format(os.sep)))
sys.stdout.write("Reading Config from  {} \n".format(CONFIGURATION_FILE))
sys.stdout.flush()
__config = configparser.ConfigParser()
__config.read(CONFIGURATION_FILE)

LOG_LEVEL = os.environ.get("LOG_LEVEL", __config.get('LOGGER', 'loglevel', fallback="DEBUG")).upper()
LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST", __config.get('LOGGER', 'loglevel', fallback=None))
LOGSTASH_PORT = os.environ.get("LOGSTASH_PORT", __config.get('LOGGER', 'loglevel', fallback=None))
LOG_HANDLER_NAME = os.environ.get("LOG_HANDLER_NAME", __config.get('LOGGER', 'loglevel', fallback="face-id"))

BASE_LOG_PATH = os.environ.get('BASE_LOG_PATH',
                               __config.get('LOGGER', 'basepath', fallback=os.path.join(os.getcwd(), "logs".format())))

if not os.path.isdir(BASE_LOG_PATH):
    os.mkdir(BASE_LOG_PATH)

BROKER_URL = os.environ.get("BROKER", __config.get('MQTT', 'BROKER', fallback="localhost"))
PORT = int(os.environ.get("BROKER_PORT", __config.get('MQTT', 'PORT', fallback="1883")))
TOPIC = os.environ.get("TOPIC", __config.get('MQTT', 'TOPIC'))
