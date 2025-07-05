import tkinter as tk
import cv2
import numpy as np
from PIL import ImageGrab, Image
from time import sleep
import ctypes
from google import genai
from dotenv import load_dotenv
from google.genai import types
from google import genai
import os
import glob
import pyaudio
import wave
import base64
from faster_whisper import WhisperModel

load_dotenv()

# Load the 'small' Whisper model for CPU, using 8-bit quantization for speed.
model = WhisperModel(
    "small",                   # model size
    device="cpu",              # run on CPU
    compute_type="int8"        # quantize weights to INT8 for ~1.5× speedup
)

# Audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
# 1) Open stream
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
frames = []

# The client reads GEMINI_API_KEY from your environment
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# the user's input text
text = ""

# ai response text
ai_text = ""

# track state of mic buttons
is_mic = None


def start_audio_recording():
    print("* recording")
    global is_mic
    is_mic = True

    # 2) Read data
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)


def stop_audio_recording():
    print("* done recording")
    global is_mic
    is_mic = False

    # 3) Close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 4) Write WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# def convert_text_to_speach():
#     global ai_text
#     # 1) Initialize client (it reads $GEMINI_API_KEY automatically)
#     global client
#     print(f'The ai says: {ai_text}')
#     # 2) Call TTS model
#     response = client.models.generate_content(
#         model="gemini-2.5-flash-preview-tts",
#         contents=ai_text,
#         config=types.GenerateContentConfig(
#             response_modalities=["AUDIO"],
#             speech_config=types.SpeechConfig(
#                 voice_config=types.VoiceConfig(
#                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                         voice_name="Kore",   # choose any supported voice
#                     )
#                 )
#             ),
#         )
#     )

#     # 3) Extract base64-encoded PCM audio
#     b64_data = response.candidates[0].content.parts[0].inline_data.data
#     if not b64_data:
#         print("No audio data returned from Gemini TTS!")
#     pcm = base64.b64decode(b64_data)

#     # 4) Save as WAV
#     with wave.open("ai_response.wav", "wb") as wf:
#         wf.setnchannels(1)              # mono
#         wf.setsampwidth(2)              # 16-bit = 2 bytes
#         wf.setframerate(24000)          # default sample rate
#         wf.writeframes(pcm)             # PCM byte data
#         print("Done saving audio file...")


def convert_speach_to_text():
    global text
    # Transcribe a WAV/MP3 file, streaming segments
    segments, info = model.transcribe(
        "output.wav",
        beam_size=5,            # higher beam for accuracy (slower)
        best_of=5               # sample multiple beams and pick best
    )

    print(f"Detected language: {info.language}")
    for segment in segments:
        start, end, local_text = segment.start, segment.end, segment.text
        # print(f"[{start:.2f}s → {end:.2f}s] {local_text}")
        print(f"start: {start}")
        print(f"end: {end}")
        print(f"Detected text: {local_text}")
        text = local_text


def start_agent():
    global ai_text
    print("Starting agent...")
    uploaded = client.files.upload(file="screenshot.png")
    final_text = "In a paragraph: " + text
    print("The text is:", final_text)
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[
            final_text,
            uploaded
        ],
    )
    # print(response.text)
    ai_text = response.text
    print("Removing screenshot...")
    print("Removing wav file...")
    os.remove("screenshot.png")
    os.remove("output.wav")  # Remove the audio file after processing
    
    # convert_text_to_speach()


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


def update_loop():
    global is_mic
    pngs = glob.glob("screenshot.png")
    if is_mic == False:
        print("Waiting for mic state...")
        if is_mic == False:
            print("'convert_speach_to_text' has been called")
            convert_speach_to_text()
        if len(pngs) != 0 and text:
            print("running loop for gui...")
            start_agent()
            is_mic = None  # Reset mic state
    # Schedule this function to run again after 1000 ms (1 second)
    root.after(1000, update_loop)


def main_gui():
    print("Starting main GUI...")
    global root
    # Main window
    root = tk.Tk()
    root.title("VisionaryTutor")
    root.geometry("200x400")

    capture = tk.Button(root, text="Capture part of screen", command=minimize_window_capture, width=22, height=5, font=("Arial", 10))
    full_capture = tk.Button(root, text="Full Capture", command=minimize_window_full, width=22, height=5, font=("Arial", 10))
    mic_on = tk.Button(root, text="Mic On", command=start_audio_recording, width=22, height=5, font=("Arial", 10))
    mic_off = tk.Button(root, text="Mic Off", command=stop_audio_recording, width=22, height=5, font=("Arial", 10))
    capture.pack(pady=5)
    full_capture.pack(pady=5)
    mic_on.pack(pady=5)
    mic_off.pack(pady=5)
    print("last line of code from main GUI...")
    update_loop()
    root.mainloop()


def main():
    # update_loop()
    main_gui()
    # root.after(1000, update_loop)  # Check again in 1000 ms (1 second)