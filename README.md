There are three files of note here.
 
cSLO_image_download_1.1.py
This is used with the Heidelberg imaging software to download images from multiple patients automatically. It reads which patients have been selected, makes folders for each patient (with OD and OS subfolders), and then exports the images to each of those folders. 
Some things to keep in mind:
You must have the Heidelberg imaging software open with patients selected
It will only export the most recent date
With our imaging protocol the OD and OS are reversed, so this program automatically switches what the imaging software thinks is "OS" to "OD" and vice versa
It uses images of the software (found in files_for_python_script) to recognize how to interact with it, so if the software is a different version than what we originally designed it for, the user will need to take replacement screenshot images

make_folders_3.0.py
If cSLO_image_download_1.1 works for you, then this is not needed because it is built into that script. However, if that script isn't working out, you can use this program to automatically create folders for each patient with OD and OS subfolders. The user can then export the images manually into these folders.

Relabel_cSLO_images_1.0.py
The Heidelberg imaging software exports the images with the following name style: 0000E_000.tif or something similar. I prefer image#_patient#_eye_image type.tif. This script assumes images are organized into eye folders labeled "OD" or "OS" and those eye folders are organized into patient folders (like what the previous two scripts make). It will look at the images to determine the image type (BAF, IRAF, etc.). 
