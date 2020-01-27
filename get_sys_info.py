import platform, socket, re, uuid, json, psutil, random
import threading
import time
from copy import deepcopy

import requests


def getSystemInfo():
    try:
        info = {}
        info["cpu_usage"] = psutil.cpu_percent(True)
        try:
            info["cpu_temparature"] = psutil.sensors_temperatures(False)
        except Exception as e:
            print(e)
            info["cpu_temparature"] = random.randrange(25, 45)
        disks = psutil.disk_partitions()
        info["no_of_disks"] = len(disks)
        info["discs"] = dict()
        for each_disk in disks:
            mount_point = each_disk.mountpoint
            usage = psutil.disk_usage(str(mount_point))
            temp_json = {str(mount_point):round((usage.used / usage.total) * 100, 2)}
            info["discs"].update(temp_json)
        ram_usage = psutil.virtual_memory()
        info["ram_usage"] = round(((ram_usage.used / ram_usage.total) * 100), 2)
        # info['platform'] = platform.system()
        # info['platform-release'] = platform.release()
        # info['platform-version'] = platform.version()
        # info['architecture'] = platform.machine()
        # info['hostname'] = socket.gethostname()
        # info['ip-address'] = socket.gethostbyname(socket.gethostname())
        # info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        # info['processor'] = platform.processor()
        # info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        # if info['platform'].lower() == 'linux':
        #     info['os_distribution'] = platform.linux_distribution()
        # elif info['platform'].lower() == 'windows':
        #     info['os_distribution'] = platform.win32_ver()
        return info
    except Exception as e:
        print("Error : {}".format(str(e)))
        raise Exception("Failed to get the system info")


# resp = getSystemInfo()
# print(resp)
url = "https://beta.ilens.io/cloud/device_manager/update_status"
# url = "http://localhost:8585/device_manager/update_status"
def background(f):
    """
     a threading decorator
    use @background above the function you want to run in the background
    :param f:
    :return:
    """

    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()

    return bg_f


@background
def update_status():
    """
    This method is for updating the device status
    :return:
    """
    # api_url = os.environ.get('apiUrl', None)
    api_url = url
    if api_url is None:
        raise Exception("Device manager api url not found in the environment variables")

    # device_id = os.environ.get('deviceId', None)
    device_id = "ilens_device_101"
    if device_id is None:
        raise Exception("Device Id not found in the environment variable")

    # ping main function returns the diagnostics data of the device
    while True:
        try:
            diagnostics_data = getSystemInfo()

            status_json = { 'status': True, 'ilens_device_id': device_id, "data": deepcopy(diagnostics_data) }
            print("API URL -----> {}".format(api_url))
            print("Status json -----> {}".format(json.dumps(status_json)))
            try:
                resp = requests.post(api_url, json=deepcopy(status_json))
            except Exception as e:
                print((str(e)))
            print("Status code after sending the status ----> : {}".format(resp.status_code))
            print("Response for submitting the status ---->: {}".format(resp.json()))
        except Exception as e:
            raise Exception("Failed to update device status : {}".format(str(e)))
        time.sleep(1 * 60)

if __name__ == '__main__':
    update_status()
