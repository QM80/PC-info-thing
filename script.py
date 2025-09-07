import os
import sys
import subprocess
import colorama
from colorama import Fore, Style, Back
import socket
import platform
import psutil
import GPUtil
import time
import tkinter as tk
import ctypes
import curses

def version():
    ver = sys.platform
    if ver == "win32":
        return "windows"
    elif ver == "linux":
        return "linux"
    elif ver == "darwin":
        return "macos"
    else:
        return ver

# memory stuff

def current_ram_usage():
    return psutil.virtual_memory().free // (1000 ** 3)


def ram_percent():

    pct = psutil.virtual_memory().percent
    if pct >= 70:
        return Fore.RED + str(pct)+ "%"
    else:
       return Fore.GREEN + str(pct)+ "%"



# other stuff
gpus = GPUtil.getGPUs()
gpu_names = [gpu.name for gpu in gpus] if gpus else ["No GPU found"]

# gpu stuff



def gpu_usage():

    GPUs = GPUtil.getGPUs()
    if GPUs:
        return round(GPUs[0].memoryUsed / 1024, 1)
    return "N/A"



def total_gpu():
    
    GPUs = GPUtil.getGPUs()
    if GPUs:
        return round(GPUs[0].memoryTotal / 1024, 1)
    return "N/A"
    


def gpu_percent():

    pct = GPUtil.getGPUs()[0].load * 100
    if pct >= 70:
        return Fore.RED + str(round(pct, 2)) + "%"
    else:
        return Fore.GREEN + str(round(pct, 2)) + "%"
    
def gpu_temp():
    temp = GPUtil.getGPUs()[0].temperature
    if temp >= 70:
        return Fore.RED + str(temp) +"°C" + Fore.WHITE
    else:
        return Fore.GREEN + str(temp) + "°C" + Fore.WHITE


# cpu stuff
cpu_name = platform.processor()
cpu_cores = psutil.cpu_count(logical=True)
cpu_Ghz = psutil.cpu_freq().max // 1000
# display stuff

def aspect_ratio():
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    
    screen_height = root.winfo_screenheight()
    return f"{screen_width}  x {screen_height}"


def get_refresh_rate():
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    hdc = user32.GetDC(0)
    VREFRESH = 116 
    refresh_rate = gdi32.GetDeviceCaps(hdc, VREFRESH)
    user32.ReleaseDC(0, hdc)
    return refresh_rate

# drive info

def total_drive():

    usage = psutil.disk_usage('/')
    total_gb = usage.total // (1000 ** 3)
    return f"{total_gb} GB"

def used_drive():

    usage = psutil.disk_usage('/')
    used_gb = usage.used // (1000 ** 3)
    return f"{used_gb} GB"


def free_drive():

    usage = psutil.disk_usage('/')
    free_gb = usage.free // (1000 ** 3)

    if free_gb <= 50:
        return Fore.RED + f"{free_gb} GB" + Fore.WHITE
    else:
        return Fore.GREEN + f"{free_gb} GB" + Fore.WHITE

    
def partitions_drive():

    usage = psutil.disk_partitions()
    return len(usage)

def pct_drive():

    usage = psutil.disk_usage('/')
    total_gb = usage.percent

    if total_gb >= 85:
        return Fore.RED + f"{total_gb} %" + Fore.WHITE
    else:
        return Fore.GREEN + f"{total_gb} %" + Fore.WHITE
    
def percent_line_drive():
    usage = psutil.disk_usage('/')
    pct = usage.percent
    bar_length = 20
    filled_length = int(bar_length * pct // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    length = len(bar)
    if length <= 17:
        bar = Fore.RED + bar + Fore.WHITE
    else:
        bar = Fore.GREEN + bar + Fore.WHITE

    return f"|{bar}| {pct_drive()}"

# device things
hostname = socket.gethostname()
os_version = platform.platform()




# programme code
while True:
    system_info = Fore.LIGHTBLUE_EX + f"""
OS   {Fore.WHITE}{version()}{Fore.LIGHTBLUE_EX}
 ├─  {Fore.WHITE}{hostname} @ {version()}{Fore.LIGHTBLUE_EX}
 ├─  {Fore.WHITE}{os_version}{Fore.LIGHTBLUE_EX}
 {Fore.CYAN}├─  {Fore.WHITE}{platform.python_version()}{Fore.CYAN}
 ├─  {Fore.WHITE}{used_drive()} / {total_drive()} | Free space: {free_drive()} | Percentage: {pct_drive()} | partitions: {partitions_drive()}  {Fore.CYAN}
 ├─  {Fore.WHITE}disk used: {percent_line_drive()}{Fore.CYAN}
 └─  {Fore.WHITE}{os.getlogin()}{Fore.CYAN}

{Fore.WHITE}
 ├─
 ├─
 ├─
 ├─
 └─

{Fore.LIGHTMAGENTA_EX}PC   {Fore.WHITE}{psutil.virtual_memory().total // (1000 ** 3)} GB RAM{Fore.LIGHTMAGENTA_EX}
 ├─  {Fore.WHITE}{cpu_name} {cpu_cores} cores {cpu_Ghz} GHz{Fore.LIGHTMAGENTA_EX} 
 ├─  {Fore.WHITE}{", ".join(gpu_names)}
 {Fore.MAGENTA}├─  {Fore.WHITE}{current_ram_usage()} GiB / {psutil.virtual_memory().total // (1000 ** 3)} GiB ({ram_percent()}{Fore.WHITE})  {Fore.MAGENTA}
 ├─  {Fore.WHITE}{gpu_usage()} GiB / {total_gpu()} GiB ({(gpu_percent())}{Fore.WHITE})  ({gpu_temp()}){Fore.MAGENTA}
 └─  {Fore.WHITE}{aspect_ratio()} @ {get_refresh_rate()} Hz {Fore.MAGENTA}
 """
    print(system_info)
    time.sleep(0.1)
    os.system('cls' if os.name == 'nt' else 'clear')
