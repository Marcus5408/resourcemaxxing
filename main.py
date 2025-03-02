from hmac import new
from torch import ne
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
        self.geometry("700x560")
        self.resizable(True, True)

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # make self transparent
        # self.attributes("-alpha", 0.9)

        self.canvas = tk.Canvas(self, bg="teal")
        self.canvas.grid(row=0, column=0, rowspan=8, sticky="nsew")
        # Bind the resize event to redraw the grid
        self.canvas.bind("<Configure>", self.on_resize)

        self.create_notebook()
        self.create_basic_widgets()
        self.create_advanced_widgets()

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

    def create_notebook(self):
        s = ttk.Style()
        s.configure("new.TFrame", background="", borderwidth=0)
        s.configure("new.TNotebook", background="", borderwidth=0)
        s.configure(
            "TNotebook.Tab", padding=[10, 5], background="lightblue", borderwidth=0
        )

        self.notebook = ttk.Notebook(self)
        self.notebook.configure(style="new.TNotebook")

        self.basic_tab = ttk.Frame(self.notebook)
        self.basic_tab.configure(style="new.TFrame")
        self.notebook.add(self.basic_tab, text="Basic Controls")

        self.advanced_tab = ttk.Frame(self.notebook)
        self.advanced_tab.configure(style="new.TFrame")
        self.notebook.add(self.advanced_tab, text="Advanced Controls")

        # Place the notebook on top of the canvas
        self.notebook.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9
        )

        # Configure styles for transparency

        # self.create_widgets_tab1()
        # self.create_widgets_tab2()

    def create_basic_widgets(self):
        self.radio_var = tk.StringVar(value="1")
        self.radio_frame = ttk.Labelframe(self.basic_tab, text="Resource Maxxing Level")
        self.radio_frame.grid(
            row=0, rowspan=2, column=0, pady=(5, 10), padx=5, sticky="w"
        )
        options = {
            "Weak Beta": "You are weak and want weak resource maxxing, this sadly isnt as taxing (get it fanum tax lol) on your resources so you can watch more skibidi!!!",
            "Lukewarm": "You like it nice and cozy you rizzer. This sends stuff over your Wi-Fi.",
            "Costco Guy": "You really like to max out your resources but you also like to save money. This is the best option for you, as just like the Double Chunk Chocolate Chip Cookies, you can get the best of both worlds.",
            "Rizzler": "Rizz Kai Cenat with your resource maxxing is pretty massive on your resources (you know what else is massive? LOWWWW TAPERR FADEEE)",
            "Cooked": "You are a cooked rizzler and you want to max out your resources to the max. This is the most taxing option. (WARNING: This may cause your drive permanent damage.)",
        }
        bold_radio = ttk.Style()
        bold_radio.configure("Bold.TRadiobutton", font=("TkDefaultFont", "10", "bold"))
        for idx, key in enumerate(options.keys(), start=1):
            text = key
            rb = ttk.Radiobutton(
                self.radio_frame,
                text=text,
                variable=self.radio_var,
                value=str(idx),
                style="Bold.TRadiobutton",
            )
            rb.grid(row=idx * 2 - 2, column=0, padx=5, pady=(5, 0), sticky="w")
            self.radio_frame.grid_rowconfigure(idx * 2 - 2, weight=1)

            # Create a label for the value
            value_label = ttk.Label(self.radio_frame, text=options[key], wraplength=400)
            value_label.grid(
                row=idx * 2 - 1, column=0, padx=20, pady=(0, 5), sticky="w"
            )
            self.radio_frame.grid_rowconfigure(idx * 2 - 1, weight=1)

        self.resourcesUsedFrame = ttk.Labelframe(self.basic_tab, text="Resources Used")
        self.resourcesUsedFrame.grid(
            row=0, column=1, pady=(5, 10), padx=5, sticky="nsew"
        )

        self.cpuLabel = ttk.Label(self.resourcesUsedFrame, text="CPU: 0%")
        self.cpuLabel.grid(row=1, column=0, sticky="w", pady=5)

        self.ramLabel = ttk.Label(self.resourcesUsedFrame, text="RAM: 0%")
        self.ramLabel.grid(row=2, column=0, sticky="w", pady=5)

        self.networkLabel = ttk.Label(self.resourcesUsedFrame, text="Network: 0%")
        self.networkLabel.grid(row=3, column=0, sticky="w", pady=5)

        self.gpuLabel = ttk.Label(self.resourcesUsedFrame, text="GPU: 0%")
        self.gpuLabel.grid(row=4, column=0, sticky="w", pady=5)

        self.diskLabel = ttk.Label(self.resourcesUsedFrame, text="Disk: 0%")
        self.diskLabel.grid(row=5, column=0, sticky="w", pady=5)

        self.apply_button = ttk.Button(
            self.basic_tab,
            text="Apply Settings",
            command=lambda: self.apply_settings("basic"),
        )
        self.apply_button.grid(row=1, column=1, padx=5, sticky="w")

        # edit column weights
        self.radio_frame.grid_columnconfigure(2, weight=2)
        self.resourcesUsedFrame.grid_columnconfigure(1, weight=1)

    def create_advanced_widgets(self):
        self.cpu_choice = tk.DoubleVar()
        self.gpu_choice = tk.DoubleVar()
        self.ram_choice = tk.DoubleVar()
        self.network_choice = tk.DoubleVar()
        self.disk_choice = tk.DoubleVar()
        self.adv_options_frame = ttk.Labelframe(
            self.advanced_tab, text="Resource Maxxing Level"
        )
        self.adv_options_frame.grid(
            row=0, rowspan=2, column=0, pady=(5, 10), padx=5, sticky="w"
        )

        options = {
            "CPU": {
                "min": 50.00,
                "max": 100.00,
            },
            "GPU": {
                "min": 50.00,
                "max": 100.00,
            },
            "RAM": {
                "min": 50.00,
                "max": 100.00,
            },
            "Network": {
                "min": 50.00,
                "max": 100.00,
            },
            "Disk": {
                "min": 50.00,
                "max": 100.00,
            },
        }

        self.scale_vars = {}
        for idx, (key, value) in enumerate(options.items()):
            label = ttk.Label(self.adv_options_frame, text=key, font=("TkDefaultFont", 10, "bold"), anchor="center")
            label.grid(row=0, column=idx, padx=5, pady=5, sticky="we")
            
            maxVal = ttk.Label(self.adv_options_frame, text=value["max"], anchor="center")
            maxVal.grid(row=1, column=idx, padx=5, pady=5, sticky="we")

            self.scale_vars[key] = tk.DoubleVar(value=value["min"])
            slider = ttk.Scale(
                self.adv_options_frame,
                from_=value["min"],
                to=value["max"],
                orient="vertical",
                length=200,
                variable=self.scale_vars[key],
            )
            slider.grid(row=2, column=idx, padx=5, pady=5, sticky="we")
            
            minVal = ttk.Label(self.adv_options_frame, text=value["min"], anchor="center")
            minVal.grid(row=3, column=idx, padx=5, pady=5, sticky="we")
            
            # set column weights
            self.adv_options_frame.grid_columnconfigure(idx, weight=1)
            self.adv_options_frame.grid_columnconfigure(idx, minsize=75)

        self.advResourcesUsedFrame = ttk.Labelframe(self.advanced_tab, text="Resources Used")
        self.advResourcesUsedFrame.grid(
            row=0, column=1, pady=(5, 10), padx=5, sticky="nsew"
        )

        self.cpuLabel = ttk.Label(self.advResourcesUsedFrame, text="CPU: 0%")
        self.cpuLabel.grid(row=1, column=0, sticky="w", pady=5)

        self.ramLabel = ttk.Label(self.advResourcesUsedFrame, text="RAM: 0%")
        self.ramLabel.grid(row=2, column=0, sticky="w", pady=5)

        self.networkLabel = ttk.Label(self.advResourcesUsedFrame, text="Network: 0%")
        self.networkLabel.grid(row=3, column=0, sticky="w", pady=5)

        self.gpuLabel = ttk.Label(self.advResourcesUsedFrame, text="GPU: 0%")
        self.gpuLabel.grid(row=4, column=0, sticky="w", pady=5)

        self.diskLabel = ttk.Label(self.advResourcesUsedFrame, text="Disk: 0%")
        self.diskLabel.grid(row=5, column=0, sticky="w", pady=5)

        self.apply_button = ttk.Button(
            self.advanced_tab,
            text="Apply Settings",
            command=lambda: self.apply_settings("advanced"),
        )
        self.apply_button.grid(row=1, column=1, padx=5, sticky="w")

        # edit column weights
        self.adv_options_frame.grid_columnconfigure(2, weight=2)
        self.advResourcesUsedFrame.grid_columnconfigure(1, weight=1)

    async def apply_settings(self, mode: str, *args):
        """
        # run all the tests and apply the settings
        """
        
        # get int from args
        # run cpu test
        from maximalizer import ResourceMaximizer
        maximizer = ResourceMaximizer()
        if mode == "basic":
            
            intensity = int(self.radio_var.get())
            await maximizer.run_basic(intensity)
        elif mode == "advanced":
            from maximalizer import ResourceMaximizer
            
            cpu = self.scale_vars["CPU"].get()
            gpu = self.scale_vars["GPU"].get()
            ram = self.scale_vars["RAM"].get()
            network = self.scale_vars["Network"].get()
            disk = self.scale_vars["Disk"].get()
            await maximizer.run_advanced(cpu=cpu, gpu=gpu, ram=ram, network=network, disk=disk)

if __name__ == "__main__":
    app = App()
    open_image("catthatresourcedmaxxed.jpg")
    app.mainloop()
