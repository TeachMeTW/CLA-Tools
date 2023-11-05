import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def load_json():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            count_responses(data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def count_responses(data):
    # Initialize counters
    yes_count = no_count = unsure_count = 0
    
    # Count the responses
    for entry in data.values():
        if entry.lower() == "yes":
            yes_count += 1
        elif entry.lower() == "no":
            no_count += 1
        elif entry.lower() == "unsure":
            unsure_count += 1
    
    # Calculate totals and percentages
    total = yes_count + no_count + unsure_count
    yes_percent = (yes_count / total * 100) if total else 0
    no_percent = (no_count / total * 100) if total else 0
    unsure_percent = (unsure_count / total * 100) if total else 0
    
    # Update the GUI with the results
    results_var.set(f"Yes: {yes_count} ({yes_percent:.2f}%)\n"
                    f"No: {no_count} ({no_percent:.2f}%)\n"
                    f"Unsure: {unsure_count} ({unsure_percent:.2f}%)")

# Set up the GUI
root = tk.Tk()
root.title("JSON Response Counter")

# Maximize the window
root.state('zoomed')

# Set up a variable to hold the results
results_var = tk.StringVar()

# Create the GUI elements
load_button = tk.Button(root, text="Load JSON", command=load_json)
results_label = tk.Label(root, textvariable=results_var)

# Layout the GUI elements
load_button.pack(pady=10)
results_label.pack(pady=10)

# Start the GUI loop
root.mainloop()
