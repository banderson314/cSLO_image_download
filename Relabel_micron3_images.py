#Relabeling Micron3 image names
#Made by Brandon Anderson, University of Pennsylvania


#This converts the file names created by the Heidelberg imaging software (i.e. 0000E_000.tif) to a
	#format that I prefer (image#_mouse#_eye_image type.tif)
#This script assumes images are organized into eye folders labeled "OD" or "OS" and those eye folders
	#are organized into mouse folders. It will ask you to select a directory that they are located in

# Supported image extensions
IMAGE_EXTENSIONS = (
	".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".webp"
)


import os
import tkinter as tk
from tkinter import filedialog
import re


def define_image_type(file_path):
	return "micron3"



average_time_for_each_mouse = 0

def is_file_name_converted(file_name):
	pattern = r"\d{3}_\w+_(OD|OS)_\w+\.tif"
	return re.match(pattern, file_name) is not None

def traverse_directory(root_dir):
	for mouse_dir in os.listdir(root_dir):
		mouse_path = os.path.join(root_dir, mouse_dir)
		if os.path.isdir(mouse_path):
			mouse_number = mouse_dir.split("_")[-1]
			for eye_dir in os.listdir(mouse_path):
				if eye_dir in ["OD", "OS"]:
					eye_path = os.path.join(mouse_path, eye_dir)
					for i, filename in enumerate(os.listdir(eye_path)):
						if filename.lower().endswith(IMAGE_EXTENSIONS):
							#if is_file_name_converted(filename):  # Check if file name is already converted
							#	continue  # Skip already converted file
							tif_file_path = os.path.join(eye_path, filename)
							image_type = define_image_type(tif_file_path)
							file_name, file_ext = os.path.splitext(filename)
							file_number = i
							new_file_name = f"{file_number:03d}_{mouse_number}_{eye_dir}_{image_type}{file_ext}"
							old_file_path = os.path.join(eye_path, filename)
							new_file_path = os.path.join(eye_path, new_file_name)
							os.rename(old_file_path, new_file_path)

def select_directory():
	root = tk.Tk()
	root.withdraw()
	dir = filedialog.askdirectory(title="Select directory")
	if dir:
		print(f"Directory selected: {dir}")
		return dir
	else:
		print("Script ended by user")
		exit()

# Main code execution starts here
dir = select_directory()


traverse_directory(dir)
print("Script complete")
