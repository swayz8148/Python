import tkinter as tk
import requests
import threading
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

api_key = 'secret_cpa8ypg82eww_318M8Yb2gAdxeYphqUYLZkpua1ainApp'
driver_path = 'chromedriver.exe'  # Update with the path to your ChromeDriver executable
window_width = 1920  # Width of the browser window
window_height = 1080  # Height of the browser window
screenshot_folder ='screenshots'

def get_phishing_report(url):
    api_url = f'https://phish.report/api/phishing/{url}'
    headers = {'Authorization': api_key}

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_phishing():
    url = url_entry.get()
    report = get_phishing_report(url)
    if report is not None:
        result_label.config(text=str(report))
    else:
        result_label.config(text='No report found for the given URL.')

def take_screenshot():
    url = url_entry.get()
    filename = os.path.join(screenshot_folder, get_site_name(url) + '.png')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.set_window_size(window_width, window_height)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  # Wait for the page to load
        driver.save_screenshot(filename)
        result_label.config(text='Screenshot captured!')
    except Exception as e:
        result_label.config(text='Error capturing screenshot.')
        print(e)
    finally:
        driver.quit()

def get_site_name(url):
    parsed_url = urlparse(url)
    site_name = parsed_url.netloc
    return site_name

# Create the main window
window = tk.Tk()
window.resizable(False, False)
window.title('Phish.report Checker')
window.geometry('400x150')

# Create URL Label
url_label = tk.Label(window, text='URL:')
url_label.grid(row=0, column=0, sticky='e')

# Create URL Entry
url_entry = tk.Entry(window)
url_entry.grid(row=0, column=1, sticky='w')

# Create Check Button
check_button = tk.Button(window, text='Check', command=check_phishing)
check_button.grid(row=1, column=0, pady=10)

# Create Screenshot Button
screenshot_button = tk.Button(window, text='Take Screenshot', command=lambda: threading.Thread(target=take_screenshot).start())
screenshot_button.grid(row=1, column=1, pady=10)

# Create Result Label
result_label = tk.Label(window, text='')
result_label.grid(row=2, column=0, columnspan=2)

# Set column weights to center the widgets
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
window.mainloop()
