from stdlog import log
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import platform
import psutil

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

def main():
    print("Hello from resource-maxxing!")
    print("its time to rizz those gpus and rev those cpus to the max!")
    open_image("catthatresourcedmaxxed.jpg")
    


if __name__ == "__main__":
    main()
