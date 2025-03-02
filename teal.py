import tkinter as tk

def draw_grid(canvas, width, height, spacing=20):
    """Draws a grid with white lines on the given canvas."""
    canvas.delete("grid_line")  # Clear previous grid lines
    for x in range(0, width, spacing):
        canvas.create_line(x, 0, x, height, fill="white", tags="grid_line")
    for y in range(0, height, spacing):
        canvas.create_line(0, y, width, y, fill="white", tags="grid_line")

def on_resize(event):
    """Redraw the grid when the window is resized."""
    draw_grid(canvas, event.width, event.height)

# Create the main window
root = tk.Tk()
root.title("Teal Grid Window")

# Create a canvas with a teal background
canvas = tk.Canvas(root, bg="teal")
canvas.pack(fill=tk.BOTH, expand=True)

# Bind the resize event to redraw the grid
canvas.bind("<Configure>", on_resize)

# Run the application
root.mainloop()
