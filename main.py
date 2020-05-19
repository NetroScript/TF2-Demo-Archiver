import easygui
import os
import string
import random
from PIL import Image
import tarfile
import shutil
import json
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count

settings = {
    "convert_images": True,
    "compress_demos": True,
    "folder_each_day": True,
}
delete = []
saving = False
tf2_path = ""
save_path = ""
demos = []
count = 0


# Load all .dem files within the demo folder into a variable
def load_files(path):
    global demos
    for (dirpath, dirnames, files) in os.walk(path):
        for file in files:
            if file.endswith(".dem"):
                if len(demos) > 0:
                    print(" " * (len("Searching for Demos - Currently: ") + len(demos[-1])), end="\r")
                print("Searching for Demos - Currently: " + os.path.join(dirpath, file), end='\r')
                demos.append(os.path.join(dirpath, file))
        if len(demos) > 0:
            print("Searching for Demos - Currently: " + demos[-1])
        print("Found " + str(len(demos)) + " Demos")
        break


# Function to process files
def process_files(files, target):
    pool = ThreadPool(cpu_count())
    to_process = []

    for i in files:
        to_process.append([i, target, str(len(demos))])

    # Run the archiving on 8 threads
    pool.map(process_file, to_process)


# Function to process a single file, allows threaded processing
def process_file(data):
    global count
    count += 1
    file = data[0]
    target = data[1]
    demo_number = count
    demo_day = ""
    file_path, file_name = os.path.split(file)
    file_name_without_extension = os.path.splitext(file_name)[0]
    files_to_be_processed = [file]
    print("Started processing demo number: " + str(demo_number) + "/" + data[2] + " ( " + file + " )")
    delete.append(file)
    if settings["folder_each_day"]:
        date = str(file_name.split("_")[0])
        if "-" in date:
            demo_day = date + "\\"
        else:
            demo_day = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + "\\"
    # Check for the tga created by TF2's own demo recording feature
    image_file = file_path + "\\" + file_name_without_extension + ".tga"
    if os.path.isfile(image_file):
        delete.append(image_file)
        if settings["convert_images"]:
            # Convert to jpg if it is a TGA
            img = Image.open(image_file)
            img.save(file_path + "\\" + directory + "\\" + file_name_without_extension + ".jpg", "JPEG", quality=100)
            files_to_be_processed.append(file_path + "\\" + directory + "\\" + file_name_without_extension + ".jpg")
        else:
            files_to_be_processed.append(image_file)

    # Check for the score screenshot by prec
    image_file = file_path + "\\" + file_name_without_extension + "_score.jpg"
    if os.path.isfile(image_file):
        delete.append(image_file)
        files_to_be_processed.append(image_file)

    # Check for the status screenshot by prec
    image_file = file_path + "\\" + file_name_without_extension + "_status.jpg"
    if os.path.isfile(image_file):
        delete.append(image_file)
        files_to_be_processed.append(image_file)

    # Check for the JSON data for f.e. killstreaks
    data_file = file_path + "\\" + file_name_without_extension + ".json"
    if os.path.isfile(data_file):
        files_to_be_processed.append(data_file)
        delete.append(data_file)

    # If the day doesn't exist as folder create it (should a day be used)
    if not os.path.exists(target + "\\" + demo_day):
        os.makedirs(target + "\\" + demo_day)

    # If demos should be compressed put all files in a tar file
    if settings["compress_demos"]:
        tar = tarfile.open(target + "\\" + demo_day + file_name_without_extension + ".tar.xz", "w:xz")
        for name in files_to_be_processed:
            new_file_name = os.path.split(name)[1]
            tar.add(name, arcname=new_file_name)
        tar.close()
    # If they shouldn't be compressed just move them
    else:
        for name in files_to_be_processed:
            new_file_name = str(os.path.split(name)[1])
            os.rename(name, target + "\\" + demo_day + new_file_name)


# Clean up after moving files, meaning deleting demos and the temporary folder
def clean_up():
    print("Starting to clean up!")
    shutil.rmtree(tf2_path + "\\" + directory)
    print("Deleted directory: '" + tf2_path + "\\" + directory + "'")
    number = 1
    total_files = str(len(delete))
    for file_to_be_deleted in delete:
        if os.path.isfile(file_to_be_deleted):
            os.remove(file_to_be_deleted)
            print(str(number) + "/" + total_files + " - Deleted file: " + file_to_be_deleted, end='\r')
        number += 1


# If a settings file exists load the saved settings from it
def load_settings():
    global saving
    global settings
    global tf2_path
    global save_path
    if os.path.isfile("./settings.json"):
        with open("./settings.json") as data_file:
            data = json.load(data_file)
        saving = data["saving"]
        settings = data["settings"]
        tf2_path = data["Paths"][0]
        save_path = data["Paths"][1]


print("Starting Jacks Demo Archiver version 0.2")

# Load settings
load_settings()

# If no settings available ask the user which settings he wants
if saving == False:

    if easygui.boolbox("Do you want to save your settings? (So you won't have to chose them again)", "", ["Yes", "No"]):
        saving = True

    print("Select your TF-Demos path")
    while not tf2_path:
        tf2_path = easygui.diropenbox("Select your TF-Demos path")
    print("Your path is: \"" + tf2_path + "\"")

    print("Select your target Save Path")
    while not save_path:
        save_path = easygui.diropenbox("Select your save path")
    print("Your path is: \"" + save_path + "\"")

    if not easygui.boolbox(
            "Do you want to convert pictures (when they are in the TGA format) (To reduce file size)? "
            "(All files which are modified will be removed from your TF2 directory)",
            "", ["Yes", "No"]):
        settings["convert_images"] = False

    if not easygui.boolbox("Do you want to compress your Demo files? (If not they will be simply moved)", "",
                           ["Yes", "No"]):
        settings["compress_demos"] = False

    if not easygui.boolbox("Should every day have it's own folder?", "", ["Yes", "No"]):
        settings["folder_each_day"] = False

    if saving:
        print("Now the settings will be saved in <current directory>\\settings.json!")
        Save = {
            "saving": saving,
            "settings": settings,
            "Paths": [tf2_path, save_path]
        }

        with open("./settings.json", 'w') as outfile:
            json.dump(Save, outfile)

print("A temporary directory will be created - it will be deleted again later on.")
directory = ''.join(
    random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))
print("The directory is: '" + directory + "'")

if not os.path.exists(tf2_path + "\\" + directory):
    os.makedirs(tf2_path + "\\" + directory)

load_files(tf2_path)
input("Press Enter to start the archiving.")
process_files(demos, save_path)
input("Press Enter to start the clean_up.")
clean_up()
