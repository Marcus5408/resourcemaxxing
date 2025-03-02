from stdlog import log
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import platform

app_version = "v0.1.0"
system_info = f"{platform.system()} {platform.architecture()[0]}"

def open_image(image_path):
    """
    Opens an image file using the default system viewer
    
    Args:
        image_path (str): Path to the image file
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    system = platform.system()
    
    if system == 'Windows':
        os.startfile(image_path)
    elif system == 'Darwin':  # macOS
        subprocess.run(['open', image_path])
    else:  # Linux and other Unix
        subprocess.run(['xdg-open', image_path])

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"ResourceMaxxing {app_version} - {system_info}")
        self.geometry("400x200")
        self.resizable(True, True)
        self.configure(bg="#327d78")
        self.create_widgets()
        

    def create_widgets(self):
        # self.label = ttk.Label(self, text="Hello, World!")
        # self.label.pack(pady=10)
        
        # self.button = ttk.Button(self, text="Click Me", command=self.on_click)
        # self.button.pack(pady=10)
        
        # self.toggle_var = tk.BooleanVar()
        # self.toggle = ttk.Checkbutton(self, text="Toggle", variable=self.toggle_var)
        # self.toggle.pack(pady=10)
        
        self.radio_var = tk.StringVar(value="1")
        self.radio_frame = tk.Frame(self, bg="#327d78", width=380)  # Increased width
        self.radio_frame.pack(pady=50, padx=20)
        self.radio_frame.grid_propagate(False)
        
        options = ["WEAK BETA - You are weak and want weak resource maxxing, this sadly isnt as taxing (get it fannum tax lol) on your resources so you can consume more skibidi media!!!", "LUKE WARM - You like it nice and cozy you rizzer. this sends stuff over your WI FI bruhhh", "RIZZLER - Rizz Kai cenat with your resource maxxing is pretty massive on your resources (you know what else is massive? LOWWWW TAPERR FADEEE)", "Option 4", "COOKED - You are a cooked rizzler and you want to max out your resources to the max. This is the most taxing option and will max out your resources to the max (WARNING THIS WILL CONTINUE TO DEATH AND USE YOUR DRIVE THIS CAN CAUSE PERMANENT DAMAGE)"]
        for idx, text in enumerate(options, start=1):
            rb = tk.Radiobutton(self.radio_frame, text=text, variable=self.radio_var, 
                      value=str(idx), bg="#327d78", fg="black", 
                      selectcolor="#327d78", activebackground="#327d78",
                      wraplength=350, justify="left")  # Added text wrapping
            rb.pack(anchor="w", pady=5)  # Added vertical padding

        self.resourcesUsedFrame = tk.Frame(self, bg="#327d78", width=380)
        self.resourcesUsedFrame.pack(pady=50, padx=20)
        self.resourcesUsedFrame.grid_propagate(False)
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="Resources Used: ", bg="#327d78", fg="black")
        self.resourcesUsedLabel.pack(anchor="w", pady=5)
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="CPU: 0%", bg="#327d78", fg="black")
        self.resourcesUsedLabel.pack(anchor="w", pady=5)
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="RAM: 0%", bg="#327d78", fg="black")
        self.resourcesUsedLabel.pack(anchor="w", pady=5)
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="Network: 0%", bg="#327d78", fg="black")
        self.resourcesUsedLabel.pack(anchor="w", pady=5)
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="GPU: 0%", bg="#327d78", fg="black")
        self.resourcesUsedLabel.pack(anchor="w", pady=5)
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="Disk: 0%", bg="#327d78", fg="black")
        self.resourcesUsedLabel.pack(anchor="w", pady=5)
        
    def on_click(self):
        log.info("Button clicked")
        messagebox.showinfo("Info", "Button clicked")
        subprocess.run(["notepad.exe"])

if __name__ == "__main__":
    app = App()
    open_image("catthatresourcedmaxxed.jpg")
    app.mainloop()