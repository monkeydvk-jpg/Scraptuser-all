import tkinter as tk
from tkinter import ttk
import sys

print("Starting UI test...")

# Create main window
root = tk.Tk()
root.title("UI Test - Adobe Stock Prompt Generator")
root.geometry("800x600")
root.configure(bg="#0d1117")

print("Window created...")

# Test basic components
main_frame = tk.Frame(root, bg="#161b22", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

print("Main frame created...")

# Title
title = tk.Label(
    main_frame,
    text="🚀 Adobe Stock Prompt Generator Pro",
    bg="#161b22",
    fg="#58a6ff",
    font=("Segoe UI", 18, "bold")
)
title.pack(pady=10)

print("Title created...")

# Test button
test_button = tk.Button(
    main_frame,
    text="🚀 START SCRAPING",
    bg="#3fb950",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    padx=30,
    pady=15,
    command=lambda: print("Button clicked!")
)
test_button.pack(pady=20)

print("Button created...")

# Status label
status = tk.Label(
    main_frame,
    text="✨ UI Test - Ready",
    bg="#161b22",
    fg="#c9d1d9",
    font=("Segoe UI", 11)
)
status.pack(pady=10)

print("Status label created...")

# Simple text area
text_area = tk.Text(
    main_frame,
    height=10,
    width=60,
    bg="#21262d",
    fg="#c9d1d9",
    font=("Segoe UI", 10)
)
text_area.pack(pady=10)
text_area.insert("1.0", "UI Test successful!\n\nIf you can see this, the basic UI components are working.\n\nNext step: Check the full application.")

print("Text area created...")

print("All components created. Starting mainloop...")

# Force window to front
root.lift()
root.attributes('-topmost', True)
root.after_idle(lambda: root.attributes('-topmost', False))

try:
    root.mainloop()
except Exception as e:
    print(f"Error in mainloop: {e}")
    input("Press Enter to continue...")
