import platform
import socket
import GPUtil
import psutil
import wmi
import humanize
import tkinter as tk
from tkinter import messagebox, font

# Function to retrieve the active GPU using WMI
def get_active_gpu_wmi():
    c = wmi.WMI()
    gpus_wmi = c.Win32_VideoController()
    for gpu in gpus_wmi:
        if gpu.AdapterRAM > 0 and gpu.VideoModeDescription != "Standard VGA Graphics Adapter":
            return gpu
    return None

# Function to retrieve network information
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

# Function to retrieve GPU information using WMI
def get_gpu_info_wmi():
    active_gpu = get_active_gpu_wmi()
    if not active_gpu:
        return ""

    gpu_info = ""
    gpu_info += f"GPU Name: {active_gpu.Name}\n"
    gpu_info += f"Adapter RAM: {humanize.naturalsize(active_gpu.AdapterRAM)}\n"
    gpu_info += f"Driver Version: {active_gpu.DriverVersion}\n"
    gpu_info += f"Video Mode Description: {active_gpu.VideoModeDescription}\n"
    return gpu_info

# Function to retrieve GPU information using GPUtil
def get_gpu_info_gputil():
    gpus_gputil = GPUtil.getGPUs()
    if not gpus_gputil:
        return ""

    gpu_info = ""
    for i, gpu in enumerate(gpus_gputil):
        gpu_info += f"GPU {i + 1} Name: {gpu.name}\n"
        gpu_info += f"GPU {i + 1} Memory Total: {gpu.memoryTotal}\n"
        gpu_info += f"GPU {i + 1} Memory Used: {gpu.memoryUsed}\n"
        gpu_info += f"GPU {i + 1} Memory Free: {gpu.memoryFree}\n"
        gpu_info += f"GPU {i + 1} Memory Utilization: {gpu.memoryUtil * 100}\n"
        gpu_info += f"GPU {i + 1} Temperature: {gpu.temperature}\n\n"
    return gpu_info

# Function to retrieve system information
def get_system_info():
    system_info = platform.uname()
    memory_info = psutil.virtual_memory()

    system_info_str = ""
    system_info_str += f"System: {system_info.system}\n"
    system_info_str += f"PC Name: {system_info.node}\n"
    system_info_str += f"Release: {system_info.release}\n"
    system_info_str += f"Version: {system_info.version}\n"
    system_info_str += f"Machine: {system_info.machine}\n"
    system_info_str += f"Processor: {system_info.processor}\n"
    system_info_str += f"Memory Total: {humanize.naturalsize(memory_info.total)}\n"
    system_info_str += f"Memory Available: {humanize.naturalsize(memory_info.available)}\n"
    return system_info_str

def Style():
    app = tk.Tk()
    app.title("System Information")
    app.geometry("400x460")
    app.resizable(False, False)

    # Customizing the GUI
    app.configure(bg="#1F1F1F")  # Dark mode background color

    # Define custom colors
    title_color = "#FFFFFF"  # White
    text_color = "#FFFFFF"  # White
    label_bg_color = "#1F1F1F"  # Dark mode background color

    # Set custom fonts
    title_font = font.Font(family="ASAP", size=12, weight="bold")
    text_font = font.Font(family="ASAP", size=10)

    # System Information Label
    system_info_label = tk.Label(app, text="System Information:", font=title_font, fg=title_color, bg=label_bg_color)
    system_info_label.pack(anchor="w")

    # System Info Text
    system_info_text = tk.Text(app, font=text_font, fg=text_color, bg=label_bg_color)
    system_info_text.pack(fill=tk.X)

    # Network Information Label
    network_info_label = tk.Label(app, text="Network Information:", font=title_font, fg=title_color, bg=label_bg_color)
    network_info_label.pack(anchor="w")

    # Network Info Text
    network_info_text = tk.Text(app, font=text_font, fg=text_color, bg=label_bg_color)
    network_info_text.pack(fill=tk.X)

    # GPU Information Labels
    gpu_info_label = tk.Label(app, text="GPU Information:", font=title_font, fg=title_color, bg=label_bg_color)
    gpu_info_label.pack(anchor="w")

    # GPU Info Text
    gpu_info_text = tk.Text(app, font=text_font, fg=text_color, bg=label_bg_color)
    gpu_info_text.pack(fill=tk.X)

    # Function to update the text widgets with system, network, and GPU information
    def update_info():
        system_info = get_system_info()
        network_info = get_network_info()
        gpu_info_wmi = get_gpu_info_wmi()
        gpu_info_gputil = get_gpu_info_gputil()

        # Clear existing text
        system_info_text.delete(1.0, tk.END)
        network_info_text.delete(1.0, tk.END)
        gpu_info_text.delete(1.0, tk.END)

        # Update text with new information
        system_info_text.insert(tk.END, system_info)
        network_info_text.insert(tk.END, network_info)
        if gpu_info_wmi:
            gpu_info_text.insert(tk.END, gpu_info_wmi)
        elif gpu_info_gputil:
            gpu_info_text.insert(tk.END, gpu_info_gputil)

    # Run the script
    run_script_button = tk.Button(app, text="Run Script", font=text_font, command=update_info)
    run_script_button.pack(pady=10)

    app.mainloop()
