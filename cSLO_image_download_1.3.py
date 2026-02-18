#Downloading cSLO images from Heidelberg Eye Explorer
#Created by Brandon Anderson, University of Pennsylvania
#Last updated on July 2025


print("Initiating script")
import os
import pyautogui
import easyocr
reader = easyocr.Reader(['en'], gpu=False, verbose=False) #This is just telling it that we want it to read English
import re
import shutil
from time import sleep
from PIL import Image
import numpy as np
import re
import tkinter as tk
from tkinter import ttk



def center_of_button(location_of_whatever):
	x_coordinate = location_of_whatever.left + round(location_of_whatever.width/2)
	y_coordinate = location_of_whatever.top + round(location_of_whatever.height/2)
	return([x_coordinate, y_coordinate])


heidelberg_logo = pyautogui.locateOnScreen('files_for_python_script/heidelbergEyeExplorer.png', grayscale=False)
heidelberg_logo = center_of_button(heidelberg_logo)
pyautogui.click(heidelberg_logo[0], heidelberg_logo[1])



#Recording how many mice there are

locations_of_black_circles = list(pyautogui.locateAllOnScreen('files_for_python_script/blackCircle.png', grayscale=True))
number_of_black_circles = len(locations_of_black_circles)
left_locations = []

for i in locations_of_black_circles:
	left_locations.append(i.left)

left_coordinates_of_interest = max(left_locations)
relevant_black_circles = []

for i in locations_of_black_circles:
	if i.left == left_coordinates_of_interest:
		relevant_black_circles.append(i)

number_of_mice = len(relevant_black_circles)
print("Number of mice found: " + str(number_of_mice))



#Identifying the mice listed on the screen

mouse_title_coordinates = []

for i in relevant_black_circles:
	x_coordinate = i.left + i.width
	y_coordinate = i.top
	mouse_title_coordinates.append([x_coordinate, y_coordinate])
	height_of_text = i.height

mice_numbers = []

for i in range(number_of_mice):
	coordinates = mouse_title_coordinates[i]
	mouse_label_image = pyautogui.screenshot('imageOfText.png', region=(coordinates[0], coordinates[1], 44, height_of_text))
	mouse_label_text = reader.readtext('imageOfText.png', detail = 0)
	edited_mouse_label = int(re.sub('\D', '', mouse_label_text[0]))
	mice_numbers.append(edited_mouse_label)

print("Mice found: ")
for i in range(number_of_mice):
	print(mice_numbers[i])

os.remove('imageOfText.png')

def edit_mouse_numbers(mice_numbers):
	root = tk.Tk()
	root.title("Confirm Mouse Numbers")
	root.attributes("-topmost", True)

	main_frame = ttk.Frame(root, padding=10)
	main_frame.grid()

	header = ttk.Label(main_frame, text="Confirm or Edit Mouse Numbers")
	header.grid(row=0, column=0, pady=(0, 5))

	entries = []

	# Entry rows
	for row, value in enumerate(mice_numbers):
		entry = ttk.Entry(main_frame, width=20)
		entry.grid(row=row, column=0, pady=1)
		entry.insert(0, str(value))
		entries.append(entry)

	def on_ok():
		try:
			for i, entry in enumerate(entries):
				mice_numbers[i] = int(entry.get())
			root.destroy()
		except ValueError:
			pass

	def on_close():
		root.destroy()
		exit()

	ok_button = ttk.Button(main_frame, text="Okay", command=on_ok)
	ok_button.grid(row=len(entries)+1, column=0, pady=(15, 0))

	root.protocol("WM_DELETE_WINDOW", on_close)
	root.bind("<Return>", lambda event: on_ok())

	# Center window on screen
	root.update_idletasks()
	window_width = root.winfo_width()
	window_height = root.winfo_height()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x = (screen_width // 2) - (window_width // 2)
	y = (screen_height // 2) - (window_height // 2)
	root.geometry(f"+{x}+{y}")

	root.mainloop()



# Launch editor window
edit_mouse_numbers(mice_numbers)


#Making the folders for the images

path = "cSLO images"

if os.path.exists(path):    #Removing the folder and everything in it if it already exists
	shutil.rmtree(path)

for i in mice_numbers:
	os.makedirs(os.path.join(path,str(i),"OD"))
	os.makedirs(os.path.join(path,str(i),"OS"))

#Loop through the list of mice:
for i in range(len(mice_numbers)):

	#Click on the mouse to go to the image page
	mouse_title_click = mouse_title_coordinates[i]
	mouse_title_click[0] = mouse_title_click[0] + 30
	mouse_title_click[1] = mouse_title_click[1] + (height_of_text/2)

	pyautogui.doubleClick(mouse_title_click[0], mouse_title_click[1])
	sleep(1)


	#Identifying the OD and OS boxes
	divider_bar_location = pyautogui.locateOnScreen('files_for_python_script/borderOfOSandODtop.png', grayscale=False)
	od_eye_box = [divider_bar_location.left + divider_bar_location.width, divider_bar_location.top + divider_bar_location.height]
	os_eye_box = [divider_bar_location.left, divider_bar_location.top + divider_bar_location.height]

	#Saving OD eye images
	pyautogui.click(od_eye_box[0], od_eye_box[1])
	with pyautogui.hold('ctrl'):        #selecting all of the images
		pyautogui.press('a')

	pyautogui.click(button='right', x=divider_bar_location.left + 90, y=divider_bar_location.top + 90)
	sleep(0.4)
	pyautogui.press('down', presses=8)
	pyautogui.press('right')
	pyautogui.press('down')
	pyautogui.press('enter')
	sleep(1)

	desktop_icon_location = pyautogui.locateOnScreen('files_for_python_script/Desktop.png', grayscale=False)
	desktop_icon_location = center_of_button(desktop_icon_location)
	pyautogui.click(desktop_icon_location[0], desktop_icon_location[1])
	sleep(0.5)

	pyautogui.write(path)
	pyautogui.press('enter')
	sleep(0.5)

	pyautogui.write(str(mice_numbers[i]))
	pyautogui.press('enter')
	sleep(0.5)

	pyautogui.write("OD")
	pyautogui.press('enter')
	sleep(0.5)

	save_button_location = pyautogui.locateOnScreen('files_for_python_script/Save.png', grayscale=False)
	save_button_location = center_of_button(save_button_location)
	pyautogui.click(save_button_location[0], save_button_location[1])
	sleep(1)



	#Saving OS eye images
	pyautogui.click(os_eye_box[0], od_eye_box[1])
	with pyautogui.hold('ctrl'):        #selecting all of the images
		pyautogui.press('a')

	above_first_os_image = pyautogui.locateOnScreen('files_for_python_script/aboveOSbox.png', grayscale=False)
	pyautogui.click(button='right', x=above_first_os_image.left + above_first_os_image.width, y=divider_bar_location.top + 90)
	sleep(0.4)
	pyautogui.press('down', presses=8)
	pyautogui.press('right')
	pyautogui.press('down')
	pyautogui.press('enter')
	sleep(1)

	desktop_icon_location = pyautogui.locateOnScreen('files_for_python_script/Desktop.png', grayscale=False)
	desktop_icon_location = center_of_button(desktop_icon_location)
	pyautogui.click(desktop_icon_location[0], desktop_icon_location[1])
	sleep(0.5)

	pyautogui.write(path)
	pyautogui.press('enter')
	sleep(0.5)

	pyautogui.write(str(mice_numbers[i]))
	pyautogui.press('enter')
	sleep(0.5)

	pyautogui.write("OS")
	pyautogui.press('enter')
	sleep(0.5)

	save_button_location = pyautogui.locateOnScreen('files_for_python_script/Save.png', grayscale=False)
	save_button_location = center_of_button(save_button_location)
	pyautogui.click(save_button_location[0], save_button_location[1])
	sleep(1)


	#Go back to the main menu
	main_menu_button_location = pyautogui.locateOnScreen('files_for_python_script/mainMenu.png', grayscale=False)
	main_menu_button_location = center_of_button(main_menu_button_location)
	pyautogui.click(main_menu_button_location[0], main_menu_button_location[1])
	sleep(1)



print("Relabeling mice", end="\r", flush=True)

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




def is_file_name_converted(file_name):
	pattern = r"\d{3}_\w+_(OD|OS)_\w+\.tif"
	return re.match(pattern, file_name) is not None

def traverse_directory(root_dir):
	count = 1
	for mouse_dir in os.listdir(root_dir):
		mouse_path = os.path.join(root_dir, mouse_dir)
		number_of_mice = len(os.listdir(root_dir))
		if os.path.isdir(mouse_path):
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
			print(f"Mice relabeled: {count}/{number_of_mice}", end="\r", flush=True)
			count += 1
	print(f"Mice relabeled: {count-1}/{number_of_mice}")

# Relabeling code execution starts here
cSLO_directory = path


traverse_directory(cSLO_directory)
