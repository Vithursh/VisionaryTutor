import tkinter as tk
import cv2
import numpy as np
from PIL import ImageGrab
from time import sleep
import ctypes


def convert_speaker_to_text(speaker):
    pass


def start_agent():
    pass


# def minimize_window_capture():
#     root.iconify()
#     print("Window minimized")
#     sleep(2)
#     print("Starting screen capture...")
#     capture__parts_of_screen()


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


# def capture__parts_of_screen():
#     # Get actual screen size (physical pixels)
#     user32 = ctypes.windll.user32
#     user32.SetProcessDPIAware()
#     screen_width = user32.GetSystemMetrics(0)
#     screen_height = user32.GetSystemMetrics(1)

#     print(f"Capturing screen: {screen_width}x{screen_height}")
#     img = np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height)))
#     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#     x, y, w, h = cv2.selectROI("Drag to select region", img, showCrosshair=True, fromCenter=False)
#     cv2.destroyAllWindows()
#     print(f"User picked region at ({x},{y}) with width={w} px and height={h} px")
#     img = np.array(ImageGrab.grab(bbox=(0, 0, screen_width, screen_height)))
#     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#     cv2.imwrite("screenshot.png", img)  # Save the screenshot
    root.deiconify()


def main_gui():
    global root
    # Main window
    root = tk.Tk()
    root.title("VisionaryTutor")
    root.geometry("200x200")

    # Widgets
    # label = tk.Label(root, text="Welcome to Tkinter")
    # label.pack(pady=10)

    # capture = tk.Button(root, text="Capture part of screen", command=minimize_window_capture, width=22, height=5, font=("Arial", 10))
    full_capture = tk.Button(root, text="Full Capture", command=minimize_window_full, width=22, height=5, font=("Arial", 10))
    # capture.pack(pady=5)
    full_capture.pack(pady=5)

    # Start the GUI loop
    root.mainloop()