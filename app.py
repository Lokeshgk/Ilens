import os
import time
import json
import requests
import threading

from scripts.utils.config import *
from scripts.utils.mqtt import MqttEngine
from scripts.utils.get_sys_info import getSystemInfo
from scripts.utils.logsetup import logger


def background(f):
    """
     a threading decorator
    use @background above the function you want to run in the background
    :param f:
    :return:
    """
    logger.debug("im a thread")

    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()

    return bg_f


@background
def get_queue():
    """
    This method will do a post request to with device_id to get the queue
    :param:
    :return:
    """
    logger.debug("In get_queue method")
    device_id = os.environ.get('deviceId', None)
    payload = {"ilens_device_id": device_id}
    response = requests.post(url="https://beta.ilens.io/cloud/device_manager/get_queue", data=json.loads(payload),
                             verify=False)
    logger.debug(str(response.status_code))
    data = response["data"]
    logger.debug(data)


@background
def update_status():
    """
    This method is for updating the device status
    :return:
    """
    logger.debug("In update status method")
    api_url = os.environ.get('apiUrl', None)
    if api_url is None:
        logger.debug(api_url)
        raise Exception("Device manager api url not found in the environment variables")

    device_id = os.environ.get('deviceId', None)
    if device_id is None:
        logger.debug(device_id)
        raise Exception("Device Id not found in the environment variable")

    # ping main function returns the diagnostics data of the device

    while True:
        try:
            diagnostics_data = getSystemInfo()
            status_json = { 'status': True, 'deviceId': device_id, "data": diagnostics_data }
            logger.debug(status_json)
            print("API URL -----> {}".format(api_url))
            print("Status json -----> {}".format(json.dumps(status_json)))
            resp = requests.post(api_url, json=status_json)
            logger.debug("Status code after sending the status ----> : {}".format(resp.status_code))
            logger.debug("Response for submitting the status ---->: {}".format(resp.json()))
            print("Status code after sending the status ----> : {}".format(resp.status_code))
            print("Response for submitting the status ---->: {}".format(resp.json()))
        except Exception as e:
            raise Exception("Failed to update device status : {}".format(str(e)))
        time.sleep(1 * 60)


if __name__ == '__main__':
    update_status()
    mqtt_obj = MqttEngine(broker=BROKER_URL, port=PORT, topic=TOPIC, client_name="test")
    mqtt_obj.forever_func()
