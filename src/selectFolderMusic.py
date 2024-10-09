from gtkDialogs import *

defaultFolder = user_music
folder = str

if defaultFolder == None or defaultFolder == "":
    folder = selectCarpet()
    if folder == None:
        folder = "None"
else:
    folder = defaultFolder

print(folder)
