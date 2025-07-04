import tkinter as tk
import cv2
import numpy as np
from PIL import ImageGrab, Image
from time import sleep
import ctypes
from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
import glob

load_dotenv()  

# The client reads GEMINI_API_KEY from your environment
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

text = ""


def convert_speach_to_text():
    pass


def start_agent():
    uploaded = client.files.upload(file="screenshot.png")

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[
            "I'm a student. Can you explain to me whats on my web browser:",
            uploaded
        ],
    )
    print(response.text)
    print("Removing screenshot...")
    os.remove("screenshot.png")


def minimize_window_capture():
    root.iconify()
    print("Window minimized")
    sleep(2)
    print("Starting screen capture...")
    capture__parts_of_screen()


def minimize_window_full():
    root.iconify()
    print("Window minimized")
    sleep(2)
    print("Starting screen capture...")
    capture_full_screen()


def capture_full_screen():
    # grab the full screen (bbox=None means entire desktop)
    screenshot = ImageGrab.grab(bbox=None)

    # show it or save it
    # screenshot.show()
    screenshot.save("screenshot.png")
    root.deiconify()


def capture__parts_of_screen():
    # Get actual screen size (physical pixels)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    print(f"Capturing screen: {screen_width}x{screen_height}")
    img = np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height)))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    x, y, w, h = cv2.selectROI("Drag to select region", img, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    print(f"User picked region at ({x},{y}) with width={w} px and height={h} px")
    img = np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height)))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("screenshot.png", img)  # Save the screenshot
    root.deiconify()


def main_gui():
    global root
    # Main window
    root = tk.Tk()
    root.title("VisionaryTutor")
    root.geometry("200x300")

    capture = tk.Button(root, text="Capture part of screen", command=minimize_window_capture, width=22, height=5, font=("Arial", 10))
    full_capture = tk.Button(root, text="Full Capture", command=minimize_window_full, width=22, height=5, font=("Arial", 10))
    mic = tk.Button(root, text="Mic On", command=convert_speach_to_text, width=22, height=5, font=("Arial", 10))
    capture.pack(pady=5)
    full_capture.pack(pady=5)
    mic.pack(pady=5)

    pngs = glob.glob("screenshot.png") # len(pngs) == 0 means we have no matches

    if len(pngs) != 0 and text:
        # Start the GUI loop
        root.mainloop()
        start_agent()