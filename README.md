# TF2-Demo-Archiver
_____________________________________________
Like the name implies - this is a script to archive your created demos.  

You save around 40% of space.  

Should work with both demos created by P-Rec and Demos created by the integrated feature of TF2.  

### Notes:  
Settings which you can set later on:

* The path of your demos
* The path where you want to archive them
* If you want to compress images (should they be .tga)
* If you just want to move all the files, or compress them all
* If you want a different folder in your archive folder for every day

## Installation
_____________________________________________

* Download this as zip and extract it to the folder where you want it to be
* Get Python (3.X)
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Check if you get a module error (like: `ImportError: No module named '<module name>'`) if so then open a console (On Windows Win + R and type cmd and press enter) and type `python -m pip install <module name>`
* Enjoy

## Changelog
_____________________________________________


### 0.2

* Added:
    * The demo archiver now utilises as many Threads as you have logical cores while archiving (meaning on the average CPU you have a ~8x Speed improvement due to using multiple processor cores)
* Improved:
    * Variable names and cleared code up generally

#### Warning:
 0.2 breaks compatibility with the settings.json, you will need to delete your previous one when upgrading.

### 0.1

* Released


## Planned features
_____________________________________________

/

