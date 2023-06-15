import platform
import socket
import GPUtil
import psutil
import wmi
import humanize
import tkinter as tk
from tkinter import messagebox, font
from tkinter.ttk import Button

def get_active_gpu_wmi():
    c = wmi.WMI()
    gpus_wmi = c.Win32_VideoController()
    for gpu in gpus_wmi:
        if gpu.AdapterRAM > 0 and gpu.VideoModeDescription != "Standard VGA Graphics Adapter":
            return gpu
    return None


def get_network_info():
    net_info = psutil.net_if_addrs()
    default_interface = next(iter(psutil.net_if_stats()))
    addresses = net_info[default_interface]

    network_info = f"Interface: {default_interface}\n"
    for address in addresses:
        if address.family == socket.AF_INET:
            network_info += f"IP Address: {address.address}\n"
            network_info += f"Netmask: {address.netmask}\n"
            network_info += f"Broadcast IP: {address.broadcast}\n"
        elif address.family == socket.AF_INET6:
            network_info += f"IPv6 Address: {address.address}\n"
            network_info += f"Netmask: {address.netmask}\n"
            network_info += f"Broadcast IP: {address.broadcast}\n"
        elif address.family == socket.AF_LINK:
            network_info += f"MAC Address: {address.address}\n"
            network_info += f"Netmask: {address.netmask}\n"
    return network_info


def get_gpu_info_wmi():
    active_gpu = get_active_gpu_wmi()
    if not active_gpu:
        return ""

    gpu_info = f"GPU Information:\n"
    gpu_info += f"GPU Name: {active_gpu.Name}\n"
    gpu_info += f"Adapter RAM: {humanize.naturalsize(active_gpu.AdapterRAM)}\n"
    gpu_info += f"Driver Version: {active_gpu.DriverVersion}\n"
    gpu_info += f"Video Mode Description: {active_gpu.VideoModeDescription}\n"
    return gpu_info


def get_gpu_info_gputil():
    gpus_gputil = GPUtil.getGPUs()
    if not gpus_gputil:
        return ""

    gpu_info = "GPU Information:\n"
    for i, gpu in enumerate(gpus_gputil):
        gpu_info += f"GPU {i + 1} Name: {gpu.name}\n"
        gpu_info += f"GPU {i + 1} Memory Total: {gpu.memoryTotal}\n"
        gpu_info += f"GPU {i + 1} Memory Used: {gpu.memoryUsed}\n"
        gpu_info += f"GPU {i + 1} Memory Free: {gpu.memoryFree}\n"
        gpu_info += f"GPU {i + 1} Memory Utilization: {gpu.memoryUtil * 100}\n"
        gpu_info += f"GPU {i + 1} Temperature: {gpu.temperature}\n\n"
    return gpu_info


def get_system_info():
    system_info = platform.uname()
    memory_info = psutil.virtual_memory()

    system_info_str = f"System Information:\n"
    system_info_str += f"System: {system_info.system}\n"
    system_info_str += f"PC Name: {system_info.node}\n"
    system_info_str += f"Release: {system_info.release}\n"
    system_info_str += f"Version: {system_info.version}\n"
    system_info_str += f"Machine: {system_info.machine}\n"
    system_info_str += f"Processor: {system_info.processor}\n"
    system_info_str += f"Memory Total: {humanize.naturalsize(memory_info.total)}\n"
    system_info_str += f"Memory Available: {humanize.naturalsize(memory_info.available)}\n\n"
    return system_info_str


def run_script():
    description = "This script provides System, Network, Storage, and GPU information."
    messagebox.showinfo("Information", description)

    choice = messagebox.askquestion("Confirmation", "Do you want to run the script?")
    if choice == "yes":
        system_info = get_system_info()
        network_info = get_network_info()
        gpu_info_wmi = get_gpu_info_wmi()
        gpu_info_gputil = get_gpu_info_gputil()

        app = tk.Tk()
        app.title("System Information")
        app.geometry("600x500")

        # Load custom font
        custom_font = font.Font(family="ASAP", size=10)

        # System Information Label
        tk.Label(app, text="System Information:", font=("ASAP", 12, "bold")).pack(anchor="w")

        # System Info Text
        system_info_label = tk.Label(app, text=system_info, font=custom_font, justify=tk.LEFT, anchor="w")
        system_info_label.pack(fill=tk.X)

        # Network Information Label
        tk.Label(app, text="Network Information:", font=("ASAP", 12, "bold")).pack(anchor="w")

        # Network Info Text
        network_info_label = tk.Label(app, text=network_info, font=custom_font, justify=tk.LEFT, anchor="w")
        network_info_label.pack(fill=tk.X)

        # GPU Information Labels
        tk.Label(app, text="GPU Information:", font=("ASAP", 12, "bold")).pack(anchor="w")
        if gpu_info_wmi:
            gpu_info_wmi_label = tk.Label(app, text=gpu_info_wmi, font=custom_font, justify=tk.LEFT, anchor="w")
            gpu_info_wmi_label.pack(fill=tk.X)
        elif gpu_info_gputil:
            gpu_info_gputil_label = tk.Label(app, text=gpu_info_gputil, font=custom_font, justify=tk.LEFT, anchor="w")
            gpu_info_gputil_label.pack(fill=tk.X)

        app.mainloop()


run_script()