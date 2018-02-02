import easygui
import os
import string
import random
from PIL import Image
import tarfile
import shutil
import json

global Settings
Settings = [0,0,0]
global saving
global delete
delete = []
global TF2Path
global SavePath
saving = 0
TF2Path = ""
SavePath = ""
demos = []
global pyf
pyf = os.path.dirname(os.path.abspath(__file__))


def loadFiles(path):
    global demos
    for (dirpath, dirnames, files) in os.walk(path):
        for file in files:
            if file.endswith(".dem"):
                if len(demos) > 0:
                    print(" " * (len("Searching for Demos - Currently: ")+len(demos[-1])), end="\r")
                print("Searching for Demos - Currently: " + os.path.join(dirpath, file), end='\r')
                demos.append(os.path.join(dirpath, file))
        if len(demos) > 0:
            print("Searching for Demos - Currently: " + demos[-1])
        print("Found " + str(len(demos)) + " Demos")
        break

		
def processFiles(files, target):
    global Settings
    z = ""
    n = 1
    lasprint = ""
    max = str(len(demos))
    for i in files:
        x = os.path.split(i)
        y = os.path.splitext(x[1])[0]
        load = [i]
        if Settings[2] == 1:
            date = x[1].split("_")[0]
            if "-" in date:
                z = date + "\\"
            else:
                z = date[0:4] + "-" + date[4:6] + "-" + date[6:8] + "\\"
        #Check for the tga created by TF2's own demo recording feature
        fil = x[0]+"\\"+y+".tga"
        if os.path.isfile(fil):
            delete.append(fil)
            if Settings[0] == 1:
                #Convert to jpg if it is a TGA
                img = Image.open(fil)
                img.save(x[0]+"\\"+directory+"\\"+y+".jpg", "JPEG", quality=100)
                print(str(n)+"/"+max + " - Converted image: " + fil , end='\r')
                load.append(x[0]+"\\"+directory+"\\"+y+".jpg")
            else:
                load.append(fil)
        #Check for the score screenshot by prec
        fil = x[0]+"\\"+y+"_score.jpg"
        if os.path.isfile(fil):
            delete.append(fil)
            load.append(fil)
        #Check for the status screenshot by prec
        fil = x[0]+"\\"+y+"_status.jpg"
        if os.path.isfile(fil):
            delete.append(fil)
            load.append(fil)
        fil = x[0]+"\\"+y+".json"
        if os.path.isfile(fil):
            load.append(fil)
            delete.append(fil)
        if not os.path.exists(target + "\\" + z):
            os.makedirs(target + "\\" + z)
        if Settings[1] == 1:
            tar = tarfile.open(target + "\\" + z + y+".tar.xz", "w:xz")
            print(" " * len(lasprint), end="\r")
            lasprint = str(n)+"/"+max + " - Starting to create archive: " + target + "\\" + z + y+".tar.xz"
            print(lasprint, end="\r")
			
            u = 1
            ul = len(load)
            for name in load:
                tname = os.path.split(name)[1]
                print(" " * len(lasprint), end="\r")
                lasprint = str(n)+"/"+max + " - Archive adding file " + str(u)+"/"+str(ul) + " : " + name
                print(lasprint, end='\r')
                tar.add(name, arcname=tname)
                u+=1
            tar.close()
            print(" " * len(lasprint), end="\r")
            lasprint = str(n)+"/"+max + " - Created archive: " + target + "\\" + z + y+".tar.xz"
            print(lasprint, end='\r')
            

        else:
            for name in load:
                tname = os.path.split(name)[1]
                os.rename(name, target + "\\" + z + tname)
                print(" " * len(lasprint), end="\r")
                lasprint = str(n)+"/"+max + " - Moved file: " + name
                print(lasprint, end='\r')
        for x in demos:
            delete.append(x)
        n+=1
    print(lasprint)


def cleanUp():
    global saving
    global Settings
    global TF2Path
    global SavePath
    print("Starting to clean up!")
    shutil.rmtree(TF2Path+"\\"+directory)
    print("Deleted directory: '" + TF2Path+"\\"+directory +"'")
    n = 1
    lastprint = ""
    un = str(len(delete))
    for fil in delete:
        if os.path.isfile(fil):
            os.remove(fil)
            print(str(n)+"/"+un+ " - Deleted file: " + fil, end='\r')
            lastprint = str(n)+"/"+un+ " - Deleted file: " + fil
        n+=1
    print(lastprint)


def LoadSettings():
    fil = pyf +"\\settings.json"
    global saving
    global Settings
    global TF2Path
    global SavePath
    if os.path.isfile(fil):
        with open(fil) as data_file:
            data = json.load(data_file)
        saving = data["saving"]
        for i in range(3):
            Settings[i] = data["Settings"][i]
        TF2Path = data["Paths"][0]
        SavePath = data["Paths"][1]

LoadSettings()

if saving == 0:

    if easygui.boolbox("Do you want to save your settings? (So you won't have to chose them again)", "", ["Yes", "No"]):
        saving = 1
    else:
        saving = 0

    print("Select your TF-Demos path")
    while not TF2Path:
        TF2Path = easygui.diropenbox("Select your TF-Demos path")
    print("Your path is: \"" + TF2Path + "\"")
	
    print("Select your target Save Path")
    while not SavePath:
        SavePath = easygui.diropenbox("Select your save path")
    print("Your path is: \"" + SavePath + "\"")

    if easygui.boolbox("Do you want to convert pictures (when they are in the TGA format) (To reduce file size)? (All files which are modified will be removed from your TF2 directory)", "", ["Yes", "No"]):
        Settings[0] = 1
    else:
        Settings[0] = 0

    if easygui.boolbox("Do you want to compress your Demo files? (If not they will be simply moved)", "", ["Yes", "No"]):
        Settings[1] = 1
    else:
        Settings[1] = 0

    if easygui.boolbox("Should every day have it's own folder?", "", ["Yes", "No"]):
        Settings[2] = 1
    else:
        Settings[2] = 0
		
    if saving == 1:
        print("Now the settings will be saved in <current directory>\settings.json!")
        Save = {
            "saving": saving,
            "Settings": [Settings[0],Settings[1],Settings[2]],
            "Paths": [TF2Path, SavePath]
        }

        with open(pyf + '\\settings.json', 'w') as outfile:
            json.dump(Save, outfile)


		
print("A temporary directory will be created - it will be deleted again later on.")
global directory
directory = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits +string.ascii_lowercase) for _ in range(10))
print("The directory is: '" + directory + "'")

if not os.path.exists(TF2Path+"\\"+directory):
    os.makedirs(TF2Path+"\\"+directory)

loadFiles(TF2Path)
input("Press Enter to start the archiving.")
processFiles(demos, SavePath)
input("Press Enter to start the cleanup.")
cleanUp()