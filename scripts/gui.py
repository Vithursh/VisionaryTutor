import tkinter as tk
# from agent import main_gui

def on_click():
    root.destroy()  # This will close the GUI window
    # Functions that start the agent
    # main_gui()


# Main window
root = tk.Tk()
root.title("Start menu")
root.geometry("300x300")

# Widgets
label = tk.Label(root, text="Welcome to Tkinter")
label.pack(pady=10)

button = tk.Button(
    root,
    text="Start",
    command=on_click,
    width=10,           # Increase width (in text units)
    height=5,           # Increase height (in text units)
    font=("Arial", 10)  # Increase font size
)
button.pack(pady=5)

# Start the GUI loop
root.mainloop()