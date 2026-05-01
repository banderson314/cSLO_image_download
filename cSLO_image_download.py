#Downloading cSLO images from Heidelberg Eye Explorer
#Created by Brandon Anderson, University of Pennsylvania


print("Initiating script")
import os
import pyautogui
import easyocr
reader = easyocr.Reader(['en'], gpu=False, verbose=False) #This is just telling it that we want it to read English
import shutil
import cv2
from time import sleep
from datetime import datetime
from PIL import Image
import numpy as np
import re
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from pyscreeze import Box
import warnings
warnings.filterwarnings("ignore", message=".*pin_memory.*")
print("Imports complete")



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

	header = ttk.Label(main_frame, text="Confirm or edit mouse numbers")
	header.grid(row=0, column=0, pady=(0, 5))

	entries = []

	# Entry rows
	for mouse, value in enumerate(mice_numbers):
		entry = ttk.Entry(main_frame, width=20)
		row = mouse + 1
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



def ask_user_what_date_to_export():
	user_chosen_date = None

	root = tk.Tk()
	root.title("Select Date to Export")

	# Instructions
	instruction_label = ttk.Label(
		root,
		text="Select a date to export images.\nChoose latest date or enter a custom date (mm/dd/yyyy).",
		justify="left"
	)
	instruction_label.pack(anchor="w", padx=10, pady=5)

	selected_option = tk.StringVar(value="latest")

	def validate_date(date_text):
		try:
			datetime.strptime(date_text, "%m/%d/%Y")
			return True
		except ValueError:
			return False

	def on_ok():
		nonlocal user_chosen_date

		if selected_option.get() == "latest":
			user_chosen_date = "latest date"
			root.destroy()
			return

		date = entry.get().strip()

		if date == "mm/dd/yyyy" or not date:
			error_label.config(text="Please enter a date.", foreground="red")
			return

		if not validate_date(date):
			error_label.config(text="Invalid date format. Use mm/dd/yyyy.", foreground="red")
			return

		user_chosen_date = date
		root.destroy()

	def on_close():
		root.destroy()
		exit()

	def on_radio_change():
		if selected_option.get() == "custom":
			entry.config(state="normal")
		else:
			entry.config(state="disabled")

	def on_entry_focus_in(event):
		if entry.get() == "mm/dd/yyyy":
			entry.delete(0, tk.END)
			entry.config(foreground="black")

	def on_entry_focus_out(event):
		if not entry.get():
			entry.insert(0, "mm/dd/yyyy")
			entry.config(foreground="gray")

	def on_key_press(event):
		# Let Enter go through so it can trigger on_ok
		if event.keysym == "Return":
			return

		# Allow control keys (Backspace, arrows, etc.)
		if len(event.char) != 1:
			return

		# Only allow digits
		if not event.char.isdigit():
			return "break"

		current = entry.get()

		# Remove placeholder if present
		if current == "mm/dd/yyyy":
			entry.delete(0, tk.END)
			current = ""

		# Prevent typing beyond 10 chars
		if len(current) >= 10:
			return "break"

		# Insert character manually
		entry.insert(tk.INSERT, event.char)

		new_text = entry.get()

		# Auto-add "/" after month and day
		if len(new_text) in (2, 5):
			entry.insert(tk.INSERT, "/")

		return "break"
	# Radio buttons
	rb_latest = ttk.Radiobutton(
		root, text="Latest Date", variable=selected_option,
		value="latest", command=on_radio_change
	)
	rb_latest.pack(anchor="w", padx=10, pady=5)

	rb_custom = ttk.Radiobutton(
		root, text="Enter Custom Date", variable=selected_option,
		value="custom", command=on_radio_change
	)
	rb_custom.pack(anchor="w", padx=10)

	# Entry
	entry = ttk.Entry(root)
	entry.pack(padx=10, pady=5, fill="x")

	entry.insert(0, "mm/dd/yyyy")
	entry.config(foreground="gray", state="disabled")

	entry.bind("<FocusIn>", on_entry_focus_in)
	entry.bind("<FocusOut>", on_entry_focus_out)
	entry.bind("<KeyPress>", on_key_press)

	# Error label
	error_label = ttk.Label(root, text="")
	error_label.pack(padx=10, pady=(0, 5))

	# OK button
	ok_button = ttk.Button(root, text="OK", command=on_ok)
	ok_button.pack(padx=10, pady=10)
	
	root.protocol("WM_DELETE_WINDOW", on_close)
	root.bind("<Return>", lambda event: on_ok())

	root.mainloop()

	return user_chosen_date

date_to_use = ask_user_what_date_to_export()




#Making the folders for the images
path = "cSLO images"

if os.path.exists(path):    #Removing the folder and everything in it if it already exists
	shutil.rmtree(path)

for i in mice_numbers:
	os.makedirs(os.path.join(path,str(i),"OD"))
	os.makedirs(os.path.join(path,str(i),"OS"))

#Loop through the list of mice:
failed_exports = []
for i in range(len(mice_numbers)):

	#Click on the mouse to go to the image page
	mouse_title_click = mouse_title_coordinates[i]
	mouse_title_click[0] = mouse_title_click[0] + 30
	mouse_title_click[1] = mouse_title_click[1] + (height_of_text/2)

	pyautogui.doubleClick(mouse_title_click[0], mouse_title_click[1])
	sleep(1)

	# Clicking on the date, as needed
	if date_to_use != "latest date":
		def find_date_on_screen(target_date):
			"""
			Returns a single PyAutoGUI-style Box object for the lowest match on screen,
			or None if no match is found.
			"""

			def normalize(text):
				return (
					text.replace("O", "0")
						.replace("l", "1")
						.replace("|", "/")
						.replace(" ", "")
				)

			def extract_matches(results, target_compact):
				matches = []

				for bbox, text, confidence in results:
					cleaned = normalize(text)

					if target_compact in cleaned.replace("/", ""):
						(tl, tr, br, bl) = bbox

						left = int(tl[0])
						top = int(tl[1])
						width = int(tr[0] - tl[0])
						height = int(bl[1] - tl[1])

						matches.append(Box(left, top, width, height))

				return matches

			def run_ocr(image):
				return reader.readtext(image, detail=1, paragraph=False)

			# -------------------------
			# SCREEN GRAB (BASE)
			# -------------------------
			img = np.array(pyautogui.screenshot())
			target_compact = target_date.replace("/", "")

			# -------------------------
			# STAGE 1: GRAYSCALE ONLY
			# -------------------------
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			results = run_ocr(gray)

			matches = extract_matches(results, target_compact)

			# fallback if needed
			if not matches:
				print("Enhancement needed")
				enhanced = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
				enhanced = cv2.convertScaleAbs(enhanced, alpha=1.3, beta=0)

				results = run_ocr(enhanced)
				matches = extract_matches(results, target_compact)

			# -------------------------
			# PICK LOWEST MATCH
			# -------------------------
			if not matches:
				return None

			lowest_match = max(matches, key=lambda box: box.top)
			
			return lowest_match

		date_location = find_date_on_screen(date_to_use)
		if date_location:
			date_location_center = center_of_button(date_location)
			pyautogui.click(date_location_center[0], date_location_center[1])
		else:
			#Go back to the main menu 
			main_menu_button_location = pyautogui.locateOnScreen('files_for_python_script/mainMenu.png', grayscale=False)
			main_menu_button_location = center_of_button(main_menu_button_location)
			pyautogui.click(main_menu_button_location[0], main_menu_button_location[1])
			sleep(1)
			failed_exports.append(mice_numbers[i])
			continue

		


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

if len(failed_exports) > 0:
    messagebox.showwarning(
        "Export Warning",
        "The following exports failed:\n" + "\n".join(map(str, failed_exports))
    )