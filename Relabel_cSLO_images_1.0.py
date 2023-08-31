#Relabeling cSLO image names
#Made by Brandon Anderson, University of Pennsylvania
#Version 1.0
#June 21, 2023

#This converts the file names created by the Heidelberg imaging software (i.e. 0000E_000.tif) to a
    #format that I prefer (image#_mouse#_eye_image type.tif)
#This script assumes images are organized into eye folders labeled "OD" or "OS" and those eye folders
    #are organized into mouse folders. It will ask you to select a directory that they are located in
#This script goes really well wtih my cSLO_image_download_X.X.py script

import time
print("Initiating script")
start_overall_time = time.time()

from PIL import Image
import easyocr
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
import re

print("OCR loading complete")

def define_image_type(file_path):
    # Open the TIFF image file
    with Image.open(file_path) as img:
        # Crop the bottom-left region of the image where the text is located
        region = img.crop((0, img.height - 33, img.width, img.height))

        # Convert the region to a NumPy array
        region_array = np.array(region)

        # Perform OCR on the region array
        results = reader.readtext(region_array)

        # Extract the recognized texts
        texts = [result[1] for result in results]
        # Extract the first item from the list
        first_text = texts[0]
        # Retrieve the text before the space
        extracted_text = first_text.split(' ')[0]

        return extracted_text

average_time_for_each_mouse = 0

def is_file_name_converted(file_name):
    pattern = r"\d{3}_\w+_(OD|OS)_\w+\.tif"
    return re.match(pattern, file_name) is not None

def traverse_directory(root_dir):
    count = 1
    time_taken_for_each_mouse = []
    for mouse_dir in os.listdir(root_dir):
        mouse_path = os.path.join(root_dir, mouse_dir)
        number_of_mice = len(os.listdir(root_dir))
        if os.path.isdir(mouse_path):
            start_time = time.time()
            mouse_number = mouse_dir.split("_")[-1]
            for eye_dir in os.listdir(mouse_path):
                if eye_dir in ["OD", "OS"]:
                    eye_path = os.path.join(mouse_path, eye_dir)
                    for filename in os.listdir(eye_path):
                        if filename.endswith(".tif"):
                            if is_file_name_converted(filename):  # Check if file name is already converted
                                continue  # Skip already converted file
                            tif_file_path = os.path.join(eye_path, filename)
                            image_type = define_image_type(tif_file_path)
                            #image_type = define_image_type()  # Modify this according to your implementation
                            file_name, file_ext = os.path.splitext(filename)
                            file_number = file_name.split("_")[-1]
                            new_file_name = f"{file_number}_{mouse_number}_{eye_dir}_{image_type}{file_ext}"
                            old_file_path = os.path.join(eye_path, filename)
                            new_file_path = os.path.join(eye_path, new_file_name)
                            os.rename(old_file_path, new_file_path)
            print(f"Mice complete: {count}/{number_of_mice}")
            count += 1
            end_time = time.time()
            time_taken_for_each_mouse.append(int(end_time - start_time))
            global average_time_for_each_mouse
            average_time_for_each_mouse = int(sum(time_taken_for_each_mouse) / len(time_taken_for_each_mouse))

def select_cSLO_directory():
    root = tk.Tk()
    root.withdraw()
    cSLO_dir = filedialog.askdirectory(title="Select cSLO directory")
    if cSLO_dir:
        print(f"Directory selected: {cSLO_dir}")
        return cSLO_dir
    else:
        print("Script ended by user")
        exit()

# Main code execution starts here
cSLO_directory = select_cSLO_directory()


traverse_directory(cSLO_directory)
print("Script complete")
print(f"Average time to process each mouse: {average_time_for_each_mouse} s")

end_overall_time = time.time()
total_overall_time = int(end_overall_time - start_overall_time)

print(f"Total time taken to completion: {total_overall_time} s")
