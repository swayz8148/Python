import platform
import socket
import GPUtil
import psutil
import wmi
import os
import humanize


def get_active_gpu_wmi():
    c = wmi.WMI()
    gpus_wmi = c.Win32_VideoController()
    for gpu in gpus_wmi:
        if gpu.AdapterRAM > 0 and gpu.VideoModeDescription != "Standard VGA Graphics Adapter":
            return gpu
    return None


def print_network_info():
    net_info = psutil.net_if_addrs()
    default_interface = next(iter(psutil.net_if_stats()))
    addresses = net_info[default_interface]

    print(f"Interface: {default_interface}")
    for address in addresses:
        if address.family == socket.AF_INET:
            print(f"IP Address: {address.address}")
            print(f"Netmask: {address.netmask}")
            print(f"Broadcast IP: {address.broadcast}")
        elif address.family == socket.AF_INET6:
            print(f"IPv6 Address: {address.address}")
            print(f"Netmask: {address.netmask}")
            print(f"Broadcast IP: {address.broadcast}")
        elif address.family == socket.AF_LINK:
            print(f"MAC Address: {address.address}")
            print(f"Netmask: {address.netmask}")


def print_gpu_info_wmi():
    active_gpu = get_active_gpu_wmi()
    if not active_gpu:
        return False

    print("GPU Information:")
    print(f"GPU Name: {active_gpu.Name}")
    print(f"Adapter RAM: {humanize.naturalsize(active_gpu.AdapterRAM)}")
    print(f"Driver Version: {active_gpu.DriverVersion}")
    print(f"Video Mode Description: {active_gpu.VideoModeDescription}")
    print()
    return True


def print_gpu_info_gputil():
    gpus_gputil = GPUtil.getGPUs()
    if not gpus_gputil:
        return

    print("GPU Information:")
    for i, gpu in enumerate(gpus_gputil):
        print(f"GPU {i + 1} Name: {gpu.name}")
        print(f"GPU {i + 1} Memory Total: {gpu.memoryTotal}")
        print(f"GPU {i + 1} Memory Used: {gpu.memoryUsed}")
        print(f"GPU {i + 1} Memory Free: {gpu.memoryFree}")
        print(f"GPU {i + 1} Memory Utilization: {gpu.memoryUtil * 100}")
        print(f"GPU {i + 1} Temperature: {gpu.temperature}")
        print()


def print_system_info():
    system_info = platform.uname()
    memory_info = psutil.virtual_memory()

    print("System Information:")
    print(f"System: {system_info.system}")
    print(f"PC Name: {system_info.node}")
    print(f"Release: {system_info.release}")
    print(f"Version: {system_info.version}")
    print(f"Machine: {system_info.machine}")
    print(f"Processor: {system_info.processor}")
    print(f"Memory Total: {humanize.naturalsize(memory_info.total)}")
    print(f"Memory Available: {humanize.naturalsize(memory_info.available)}")
    print()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome():
    clear_console()
    print("Welcome to my script. This script shows you your System, Network, Storage, and GPU information")
    print()
    print_system_info()
    print("Network Information:")
    print_network_info()
    print()
    if not print_gpu_info_wmi():
        print_gpu_info_gputil()


def run_script():
    description = "This script provides System, Network, Storage, and GPU information."
    print(description)
    print()

    choice = input("Do you want to run the script? (yes or no): ")
    if choice.lower() == "yes":
        welcome()
    else:
        print("Script execution canceled.")


if __name__ == "__main__":
    run_script()