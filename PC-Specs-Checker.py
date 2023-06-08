import platform
import socket
import GPUtil
import psutil
import wmi
import os


def get_active_gpu_wmi():
    c = wmi.WMI()
    gpus_wmi = c.Win32_VideoController()
    for gpu in gpus_wmi:
        if gpu.AdapterRAM > 0 and gpu.VideoModeDescription != "Standard VGA Graphics Adapter":
            return gpu

    return None


def print_network_info():
    net_info = psutil.net_if_addrs()
    default_interface = list(psutil.net_if_stats().keys())[0]
    addresses = net_info[default_interface]

    print(f"  Interface: {default_interface}")
    for address in addresses:
        if address.family == socket.AF_INET:
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif address.family == socket.AF_INET6:
            print(f"  IPv6 Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif address.family == socket.AF_LINK:
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")


def print_gpu_info_wmi():
    active_gpu = get_active_gpu_wmi()
    if not active_gpu:
        return False

    print("GPU Information:")
    print(f"  GPU Name: {active_gpu.Name}")
    print(f"  Adapter RAM: {active_gpu.AdapterRAM} bytes")
    print(f"  Driver Version: {active_gpu.DriverVersion}")
    print(f"  Video Mode Description: {active_gpu.VideoModeDescription}")
    print()

    return True


def print_gpu_info_gputil():
    gpus_gputil = GPUtil.getGPUs()
    if not gpus_gputil:
        return

    print("GPU Information:")
    for i, gpu in enumerate(gpus_gputil):
        print(f"  GPU {i+1} Name: {gpu.name}")
        print(f"  GPU {i+1} Memory Total: {gpu.memoryTotal}")
        print(f"  GPU {i+1} Memory Used: {gpu.memoryUsed}")
        print(f"  GPU {i+1} Memory Free: {gpu.memoryFree}")
        print(f"  GPU {i+1} Memory Utilization: {gpu.memoryUtil * 100}")
        print(f"  GPU {i+1} Temperature: {gpu.temperature}")
        print()


def print_system_info():
    system_info = platform.uname()
    print("System Information:")
    print(f"  System: {system_info.system}")
    print(f"  PC Name: {system_info.node}")
    print(f"  Release: {system_info.release}")
    print(f"  Version: {system_info.version}")
    print(f"  Machine: {system_info.machine}")
    print(f"  Processor: {system_info.processor}")
    print()


def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def welcome(user):
    clear_console()
    print("Welcome, " + user)
    print()
    print_system_info()
    print("Network Information:")
    print_network_info()
    print()

    if not print_gpu_info_wmi():
        print_gpu_info_gputil()


if __name__ == "__main__":
    stored_username = "Swayz"
    stored_password = "123"

    print("Username:")
    username = input().strip()
    print("Password:")
    password = input().strip()

    if username == stored_username and password == stored_password:
        welcome(username)
    else:
        print("Invalid username or password.")
