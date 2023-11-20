import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import json

# Define the categories and corresponding keys
categories = {
    '[': 'yes',
    ']': 'no',
    '\\': 'unsure'
}

# Initialize the main application window
root = tk.Tk()
root.title("Image Categorizer")

# Make the window full screen
root.attributes('-fullscreen', True)

# Label for displaying images
image_label = tk.Label(root)
image_label.pack()

# Label for displaying the progress and image info
info_label = tk.Label(root, text="Choose a folder to start")
info_label.pack()

# Label for displaying the statistics
stats_label = tk.Label(root, text="")
stats_label.pack()

# List to hold the categorization data and the image list
categorizations = {}
image_list = []
current_image_index = 0
filtered_image_list = []
review_mode = False
current_category = 'unsorted'

# Function to update info label based on the category
def update_info_label():
    if review_mode:
        image_name = os.path.basename(filtered_image_list[current_image_index])
        progress = f"{current_image_index + 1} of {len(filtered_image_list)}"
    else:
        image_name = os.path.basename(image_list[current_image_index])
        progress = f"{current_image_index + 1} of {len(image_list)}"
    
    category = categorizations.get(image_name, "Not categorized")
    stats = calculate_stats()
    info_label.config(text=f"Image: {image_name} | Category: {category} | Progress: {progress}")
    stats_label.config(text=f"Stats: {stats}")

# Calculate statistics
def calculate_stats():
    total_categorized = len(categorizations)
    counts = {cat: len([name for name in categorizations.values() if name == cat]) for cat in categories.values()}
    # Check if there are any categorized images to avoid division by zero
    if total_categorized > 0:
        percentages = {cat: (count / total_categorized * 100) for cat, count in counts.items()}
    else:
        percentages = {cat: 0 for cat in categories.values()}
    stats_string = " | ".join([f"{cat}: {counts[cat]} ({percentages[cat]:.2f}%)" for cat in categories.values()])
    return stats_string

# Function to choose folder and load images
def choose_folder_and_load_images():
    global image_list, current_image_index, review_mode
    review_mode = False
    current_image_index = 0
    folder_selected = filedialog.askdirectory(initialdir=os.getcwd())  # Start in the current working directory
    if folder_selected:
        load_images(folder_selected)
        load_progress('FullData.json')
        display_current_image()
        update_info_label()

# Load image file names from a folder
def load_images(folder_path):
    global image_list
    image_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_list.sort()  # Sort the file list

# Display the current image
def display_current_image():
    global current_image_index, image_list, filtered_image_list, review_mode
    if review_mode:
        img_path = filtered_image_list[current_image_index]
    else:
        img_path = image_list[current_image_index]
    img = Image.open(img_path)
    img.thumbnail((800, 600), Image.ANTIALIAS)  # Resize if needed
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference
    update_info_label()

# Load progress from the JSON file
def load_progress(file_path):
    global categorizations, current_image_index
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            categorizations = json.load(file)
        # Update the current index to the first uncategorized image
        for i, img in enumerate(image_list):
            if os.path.basename(img) not in categorizations:
                current_image_index = i
                break
        else:
            current_image_index = len(image_list) - 1  # All images are categorized
    else:
        current_image_index = 0  # No progress file, start from the beginning

# Handle key press event
def categorize_image(event):
    global current_image_index, categorizations, image_list, review_mode, filtered_image_list
    if event.char in categories:
        if review_mode:
            image_name = os.path.basename(filtered_image_list[current_image_index])
        else:
            image_name = os.path.basename(image_list[current_image_index])
        categorizations[image_name] = categories[event.char]
        save_categorizations('FullData.json')
        if review_mode:
            filtered_image_list.pop(current_image_index)
            if current_image_index >= len(filtered_image_list):
                current_image_index = len(filtered_image_list) - 1
        else:
            move_to_next_image()

# Move to next image
def move_to_next_image():
    global current_image_index, image_list, review_mode, filtered_image_list
    if review_mode:
        current_image_index = min(current_image_index + 1, len(filtered_image_list) - 1)
    else:
        current_image_index = min(current_image_index + 1, len(image_list) - 1)
    display_current_image()

# Move to previous image
def move_to_previous_image():
    global current_image_index, review_mode, filtered_image_list
    if review_mode:
        current_image_index = max(current_image_index - 1, 0)
    else:
        current_image_index = max(current_image_index - 1, 0)
    display_current_image()

# Save categorizations to a JSON file
def save_categorizations(file_path):
    with open(file_path, 'w') as file:
        json.dump(categorizations, file, indent=4)

# Save progress when the application closes
def on_closing():
    save_categorizations('FullData.json')
    root.destroy()

# Bind keys to the categorize_image function and arrow key functions
root.bind('<Left>', lambda event: move_to_previous_image())
root.bind('<Right>', lambda event: move_to_next_image())
for key in categories:
    root.bind(key, categorize_image)

# Set the on_closing function to be called when the window is closed
root.protocol("WM_DELETE_WINDOW", on_closing)

# Button for choosing a folder
choose_folder_button = tk.Button(root, text="Choose Folder", command=choose_folder_and_load_images)
choose_folder_button.pack()

# New buttons to navigate by category
yes_button = tk.Button(root, text="Review Yes", command=lambda: filter_images_by_category('yes'))
no_button = tk.Button(root, text="Review No", command=lambda: filter_images_by_category('no'))
unsure_button = tk.Button(root, text="Review Unsure", command=lambda: filter_images_by_category('unsure'))
unsorted_button = tk.Button(root, text="Review Unsorted", command=lambda: filter_images_by_category('unsorted'))

yes_button.pack()
no_button.pack()
unsure_button.pack()
unsorted_button.pack()

# New function to filter images by category
def filter_images_by_category(category):
    global filtered_image_list, current_image_index, current_category, review_mode
    review_mode = True
    current_category = category
    if category == 'unsorted':
        filtered_image_list = [img for img in image_list if os.path.basename(img) not in categorizations]
    else:
        filtered_image_list = [img for img in image_list if categorizations.get(os.path.basename(img), 'Not categorized') == category]
    current_image_index = 0
    display_current_image()

# Start the GUI loop
root.mainloop()
