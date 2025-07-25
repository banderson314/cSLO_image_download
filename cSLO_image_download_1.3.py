#Downloading cSLO images from Heidelberg Eye Explorer
#Created by Brandon Anderson, University of Pennsylvania
#Version 1.3
#Last updated on July 2025


print("Initiating script")
#Imports
import os
import pyautogui
import easyocr
reader = easyocr.Reader(['en'], gpu=False, verbose=False) #This is just telling it that we want it to read English
import re
import shutil
#from pynput import mouse
from time import sleep
from PIL import Image
import numpy as np
import re

#Functions

def centerOfButton(locationOfWhatever):
    xCoordinate = locationOfWhatever.left + round(locationOfWhatever.width/2)
    yCoordinate = locationOfWhatever.top + round(locationOfWhatever.height/2)
    return([xCoordinate, yCoordinate])

#Maximize screen?

heidelbergLogo = pyautogui.locateOnScreen('files_for_python_script/heidelbergEyeExplorer.png', grayscale=False)
heidelbergLogo = centerOfButton(heidelbergLogo)
pyautogui.click(heidelbergLogo[0], heidelbergLogo[1])

#maximizebutton = pyautogui.locateOnScreen('files_for_python_script/maximize.png', grayscale=False)
#maximizebutton = centerOfButton(maximizebutton)
#pyautogui.click(maximizebutton[0], maximizebutton[1])
#sleep(1)


#Recording how many mice there are

locationsOfBlackCircles = list(pyautogui.locateAllOnScreen('files_for_python_script/blackCircle.png', grayscale=True))
numberOfBlackCircles = len(locationsOfBlackCircles)
leftLocations = []

for i in locationsOfBlackCircles:
    leftLocations.append(i.left)

leftCoordinatesOfInterest = max(leftLocations)
relevantBlackCircles = []

for i in locationsOfBlackCircles:
    if i.left == leftCoordinatesOfInterest:
        relevantBlackCircles.append(i)

numberOfMice = len(relevantBlackCircles)
print("Number of mice found: " + str(numberOfMice))



#Identifying the mice listed on the screen

mouseTitleCoordinates = []

for i in relevantBlackCircles:
    xCoordinate = i.left + i.width
    yCoordinate = i.top
    mouseTitleCoordinates.append([xCoordinate, yCoordinate])
    heightOfText = i.height

miceNumbers = []

for i in range(numberOfMice):
    coordinates = mouseTitleCoordinates[i]
    mouseLabelImage = pyautogui.screenshot('imageOfText.png', region=(coordinates[0], coordinates[1], 44, heightOfText))
    mouseLabelText = reader.readtext('imageOfText.png', detail = 0)
    editedMouseLabel = int(re.sub('\D', '', mouseLabelText[0]))
    miceNumbers.append(editedMouseLabel)

print("Mice found: ")
for i in range(numberOfMice):
    print(miceNumbers[i])

os.remove('imageOfText.png')


#Making the folders for the images

path = "cSLO images"

if os.path.exists(path):    #Removing the folder and everything in it if it already exists
    shutil.rmtree(path)

for i in miceNumbers:
    os.makedirs(os.path.join(path,str(i),"OD"))
    os.makedirs(os.path.join(path,str(i),"OS"))

#Loop through the list of mice:
for i in range(len(miceNumbers)):

    #Click on the mouse to go to the image page
    mouseTitleClick = mouseTitleCoordinates[i]
    mouseTitleClick[0] = mouseTitleClick[0] + 30
    mouseTitleClick[1] = mouseTitleClick[1] + (heightOfText/2)

    pyautogui.doubleClick(mouseTitleClick[0], mouseTitleClick[1])
    sleep(1)


    #Identifying the OD and OS boxes
    dividerBarLocation = pyautogui.locateOnScreen('files_for_python_script/borderOfOSandODtop.png', grayscale=False)
    ODEyeBox = [dividerBarLocation.left + dividerBarLocation.width, dividerBarLocation.top + dividerBarLocation.height]
    OSEyeBox = [dividerBarLocation.left, dividerBarLocation.top + dividerBarLocation.height]

    #Saving OD eye images
    pyautogui.click(ODEyeBox[0], ODEyeBox[1])
    with pyautogui.hold('ctrl'):        #selecting all of the images
        pyautogui.press('a')

    pyautogui.click(button='right', x=dividerBarLocation.left + 90, y=dividerBarLocation.top + 90)
    sleep(0.4)
    pyautogui.press('down', presses=8)
    pyautogui.press('right')
    pyautogui.press('down')
    pyautogui.press('enter')
    sleep(1)

    desktopIconLocation = pyautogui.locateOnScreen('files_for_python_script/Desktop.png', grayscale=False)
    desktopIconLocation = centerOfButton(desktopIconLocation)
    pyautogui.click(desktopIconLocation[0], desktopIconLocation[1])
    sleep(0.5)

    pyautogui.write(path)
    pyautogui.press('enter')
    sleep(0.5)

    pyautogui.write(str(miceNumbers[i]))
    pyautogui.press('enter')
    sleep(0.5)

    pyautogui.write("OD")
    pyautogui.press('enter')
    sleep(0.5)

    saveButtonLocation = pyautogui.locateOnScreen('files_for_python_script/Save.png', grayscale=False)
    saveButtonLocation = centerOfButton(saveButtonLocation)
    pyautogui.click(saveButtonLocation[0], saveButtonLocation[1])
    sleep(1)



    #Saving OS eye images
    pyautogui.click(OSEyeBox[0], ODEyeBox[1])
    with pyautogui.hold('ctrl'):        #selecting all of the images
        pyautogui.press('a')

    aboveFirstOSimage = pyautogui.locateOnScreen('files_for_python_script/aboveOSbox.png', grayscale=False)
    pyautogui.click(button='right', x=aboveFirstOSimage.left + aboveFirstOSimage.width, y=dividerBarLocation.top + 90)
    sleep(0.4)
    pyautogui.press('down', presses=8)
    pyautogui.press('right')
    pyautogui.press('down')
    pyautogui.press('enter')
    sleep(1)

    desktopIconLocation = pyautogui.locateOnScreen('files_for_python_script/Desktop.png', grayscale=False)
    desktopIconLocation = centerOfButton(desktopIconLocation)
    pyautogui.click(desktopIconLocation[0], desktopIconLocation[1])
    sleep(0.5)

    pyautogui.write(path)
    pyautogui.press('enter')
    sleep(0.5)

    pyautogui.write(str(miceNumbers[i]))
    pyautogui.press('enter')
    sleep(0.5)

    pyautogui.write("OS")
    pyautogui.press('enter')
    sleep(0.5)

    saveButtonLocation = pyautogui.locateOnScreen('files_for_python_script/Save.png', grayscale=False)
    saveButtonLocation = centerOfButton(saveButtonLocation)
    pyautogui.click(saveButtonLocation[0], saveButtonLocation[1])
    sleep(1)


    #Go back to the main menu
    mainMenuButtonLocation = pyautogui.locateOnScreen('files_for_python_script/mainMenu.png', grayscale=False)
    mainMenuButtonLocation = centerOfButton(mainMenuButtonLocation)
    pyautogui.click(mainMenuButtonLocation[0], mainMenuButtonLocation[1])
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

# Main code execution starts here
cSLO_directory = path


traverse_directory(cSLO_directory)
