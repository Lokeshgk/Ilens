import json
import paho.mqtt.client as mqtt
from scripts.utils.logsetup import logger
from scripts.core.docker_engine import DockerEngine


def on_connect(client, userdata, flags, rc):
    logger.info(" {} connected to {} With Result Code {} ".format(client, userdata, rc))


def test(client, userdata, message):
    logger.info("Started reading messages")
    logger.debug(type(message.payload.decode()))
    logger.info(" Received Message {}".format(message.payload.decode()))


def on_message(client, userdata, message):
    logger.info("Started reading messages")
    data = json.loads(message.payload.decode())
    print(data)
    logger.debug(type(data))
    if data["task"] == "runimage":
        print("Running image")
        DockerEngine().run_image(data)
    elif data["task"] == 'pull':
        DockerEngine().pull_image(data)


class MqttEngine:
    def __init__(self, broker, port, topic, client_name, on_message=on_message, on_connect=on_connect):
        self.broker = broker
        self.port = int(port)
        self.topic = topic
        self.client_name = client_name
        self.client = mqtt.Client()
        # self.client = mqtt.Client(self.client_name)
        self.client.connect(host=self.broker, port=self.port)
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.subscribe(topic)

    def send_data(self, data):
        self.client.publish(self.topic, json.dumps(data))

    def forever_func(self):
        self.client.loop_forever()
