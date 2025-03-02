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

    if system == "Windows":
        os.startfile(image_path)
    elif system == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    else:  # Linux and other Unix
        subprocess.run(["xdg-open", image_path])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"ResourceMaxxing {app_version} - {system_info}")
        self.geometry("400x200")
        self.resizable(True, True)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self, bg="teal")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        # Bind the resize event to redraw the grid
        self.canvas.bind("<Configure>", self.on_resize)
        self.create_widgets()

    def draw_bg(self, width, height, spacing=20):
        """Draws a grid with white lines on the given canvas."""
        self.canvas.delete("grid_line")  # Clear previous grid lines
        for x in range(0, width, spacing):
            self.canvas.create_line(x, 0, x, height, fill="white", tags="grid_line")
        for y in range(0, height, spacing):
            self.canvas.create_line(0, y, width, y, fill="white", tags="grid_line")

    def on_resize(self, event):
        """Redraw the grid when the window is resized."""
        self.draw_bg(event.width, event.height)

    def create_widgets(self):
        self.radio_var = tk.StringVar(value="1")
        self.radio_frame = tk.Frame(self)
        self.radio_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
        self.radio_frame.grid_propagate(False)

        options = [
            "WEAK BETA - You are weak and want weak resource maxxing, this sadly isnt as taxing (get it fannum tax lol) on your resources so you can consume more skibidi media!!!",
            "LUKE WARM - You like it nice and cozy you rizzer. this sends stuff over your WI FI bruhhh",
            "COSTCO GUY - You really like to max out your resources but you also like to save money. This is the best option for you, as just like the Double Chunk Chocolate Chip Cookies, you can get the best of both worlds.",
            "RIZZLER - Rizz Kai cenat with your resource maxxing is pretty massive on your resources (you know what else is massive? LOWWWW TAPERR FADEEE)",
            "COOKED - You are a cooked rizzler and you want to max out your resources to the max. This is the most taxing option and will max out your resources to the max (WARNING THIS WILL CONTINUE TO DEATH AND USE YOUR DRIVE THIS CAN CAUSE PERMANENT DAMAGE)",
        ]
        for idx, text in enumerate(options, start=1):
            rb = tk.Radiobutton(
                self.radio_frame,
                text=text,
                variable=self.radio_var,
                value=str(idx),
                wraplength=350,
                justify="left",
            )  # Added text wrapping
            rb.pack(anchor="w", pady=5)  # Added vertical padding

        self.resourcesUsedFrame = tk.Frame(self, width=380)
        self.resourcesUsedFrame.grid(row=2, column=0, pady=50, padx=20, sticky="nsew")
        self.resourcesUsedFrame.grid_propagate(False)
        
        self.resourcesUsedLabel = tk.Label(self.resourcesUsedFrame, text="Resources Used: ")
        self.resourcesUsedLabel.grid(row=0, column=0, sticky="w", pady=5)
        
        self.cpuLabel = tk.Label(self.resourcesUsedFrame, text="CPU: 0%")
        self.cpuLabel.grid(row=1, column=0, sticky="w", pady=5)
        
        self.ramLabel = tk.Label(self.resourcesUsedFrame, text="RAM: 0%")
        self.ramLabel.grid(row=2, column=0, sticky="w", pady=5)
        
        self.networkLabel = tk.Label(self.resourcesUsedFrame, text="Network: 0%")
        self.networkLabel.grid(row=3, column=0, sticky="w", pady=5)
        
        self.gpuLabel = tk.Label(self.resourcesUsedFrame, text="GPU: 0%")
        self.gpuLabel.grid(row=4, column=0, sticky="w", pady=5)
        
        self.diskLabel = tk.Label(self.resourcesUsedFrame, text="Disk: 0%")
        self.diskLabel.grid(row=5, column=0, sticky="w", pady=5)

    def on_click(self):
        log.info("Button clicked")
        messagebox.showinfo("Info", "Button clicked")
        subprocess.run(["notepad.exe"])


if __name__ == "__main__":
    app = App()
    open_image("catthatresourcedmaxxed.jpg")
    app.mainloop()
