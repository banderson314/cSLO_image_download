#Downloading cSLO images from Heidelberg Eye Explorer
#Created by Brandon Anderson, University of Pennsylvania
#Version 1.1
#Last updated on March 27, 2023


#Imports
import os
import pyautogui
import easyocr
reader = easyocr.Reader(['en']) #This is just telling it that we want it to read English
import re
import shutil
#from pynput import mouse
from time import sleep


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
