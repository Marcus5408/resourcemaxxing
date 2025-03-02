from stdlog import log
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import platform

app_version = "v0.1.0"
system_info = f"{platform.system()} {platform.architecture()[0]}"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"ResourceMaxxing {app_version} - {system_info}")
        self.geometry("400x200")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Hello, World!")
        self.label.pack(pady=10)
        
        self.button = ttk.Button(self, text="Click Me", command=self.on_click)
        self.button.pack(pady=10)
        
        self.toggle_var = tk.BooleanVar()
        self.toggle = ttk.Checkbutton(self, text="Toggle", variable=self.toggle_var)
        self.toggle.pack(pady=10)

    def on_click(self):
        log.info("Button clicked")
        messagebox.showinfo("Info", "Button clicked")
        subprocess.run(["notepad.exe"])

if __name__ == "__main__":
    app = App()
    app.mainloop()