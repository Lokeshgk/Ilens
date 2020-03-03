import platform, socket, re, uuid, json, psutil, random, os, threading,requests, time


def getSystemInfo():
    try:
        info = {}
        # info["cpu_usage"] = psutil.cpu_percent(True)
        try:
            info["cpu_temparature"] = psutil.sensors_temperatures(False)
        except Exception as e:
            print(e)
            info["cpu_temparature"] = random.randrange(25, 40)
        disks = psutil.disk_partitions()
        info["no_of_disks"] = len(disks)
        # info["discs"] = dict()
        # for each_disk in disks:
        #     mount_point = each_disk.mountpoint
        #     usage = psutil.disk_usage(str(mount_point))
        #     temp_json = {str(mount_point):round((usage.used / usage.total) * 100, 2)}
        #     info["discs"].update(temp_json)
        ram_usage = psutil.virtual_memory()
        info["ram_usage"] = round(((ram_usage.used / ram_usage.total) * 100), 2)
        info['platform'] = platform.system()
        info['platform-version'] = platform.version()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        try:
            info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        except Exception as e:
            info['mac-address'] = ""
        p = os.popen("df -Th")
        disk_list = { }
        i = 0
        while 1:
            try:
                i = i + 1
                line = p.readline()
                if "/dev/" in line.split()[0]:
                    disk_list[line.split()[0]] = line.split()[0:7]
            except:
                break
        info["discs"] = disk_list
        info["cpu_usage"] = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
        # info['platform-release'] = platform.release()
        # info['architecture'] = platform.machine()
        # info['hostname'] = socket.gethostname()
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


