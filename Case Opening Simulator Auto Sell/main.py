import keyboard
import pyautogui
import cv2
import numpy as np
import time

capture_key = 'f2'
pause_key = 'f3'
capturing = False
green_button_image = None
paused = False

def capture_green_button():
    global capturing, green_button_image
    capturing = True

def toggle_pause():
    global paused
    paused = not paused

def on_key_press(event):
    global capturing, green_button_image
    if event.name == capture_key:
        if not capturing:
            capturing = True
        else:
            capturing = False
            green_button_image = None
    elif event.name == pause_key:
        toggle_pause()

keyboard.on_press(on_key_press)

click_delay = 2
next_click_time = time.time() + click_delay

template = cv2.imread('sell_for_button_template.png', cv2.IMREAD_GRAYSCALE)
template_width, template_height = template.shape[::-1]

while True:
    if not paused:
        if capturing:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            cv2.imshow('Capture', screenshot)

            green_button_image = screenshot

        if green_button_image is not None and time.time() >= next_click_time:
            result = cv2.matchTemplate(green_button_image, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.8)

            for loc in zip(*locations[::-1]):
                button_center_x = loc[0] + template_width // 2
                button_center_y = loc[1] + template_height // 2
                pyautogui.moveTo(button_center_x, button_center_y)
                pyautogui.mouseDown()

                while pyautogui.position() != (button_center_x, button_center_y):
                    time.sleep(0.1)

                pyautogui.mouseUp()

                time.sleep(0.5)

            next_click_time = time.time() + click_delay

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()