# cSLO Image Download and Organization

There are three files of note in this repository:

## `cSLO_image_download.py`

This script is designed to work with the Heidelberg imaging software to automatically download images from multiple selected patients.

The script:

- Reads which patients are currently selected in the Heidelberg imaging software
- Creates a folder for each patient, with `OD` and `OS` subfolders
- Automatically exports the images into the appropriate patient and eye folders

### Things to keep in mind

- The Heidelberg imaging software must be open with the desired patients selected before running the script.
- With our imaging protocol, the OD and OS labels are reversed in the Heidelberg software. This script automatically switches the software's `OS` images to `OD` and vice versa.
- The script uses screenshots of the Heidelberg software, located in `files_for_python_script`, to recognize and interact with different elements of the software. If the software is updated to a different version than the one this script was designed for, replacement screenshots may need to be taken.

## `make_folders.py`

If `cSLO_image_download_1.3.py` is working properly, this script is not necessary because folder creation is built into the download script.

If the download script is not working, however, this script can be used to automatically create a folder for each patient, with `OD` and `OS` subfolders. Images can then be exported manually from the Heidelberg imaging software into the appropriate folders.

## `Relabel_cSLO_images.py`

The Heidelberg imaging software exports images using filenames such as:

`0000E_000.tif`

I prefer images to use the following naming convention:

`image#_patient#_eye_image type.tif`

This script assumes that images are organized into patient folders, with `OD` and `OS` eye subfolders, as created by the previous two scripts.

The script examines each image to determine its image type (e.g., BAF, IRAF) and then renames the images according to the preferred naming convention.

This functionality has since been incorporated into the main `cSLO_image_download.py` script, so this script is generally only needed when relabeling older images.