import src.timeliner as timeliner
import src.subtitlePopup as subtitlePopup
import src.music as music
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
from src.colors import *


# OPENING A SRT FILE
file_path = filedialog.askopenfilename()
file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
file_url = urllib.parse.unquote(file_url)

print(file_url)
timeliner.srt_path = file_url

# OPENING A MUSIC FILE COMPATIBLE WITH pygame.mixer
file_path = filedialog.askopenfilename()
music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
music_url = urllib.parse.unquote(music_url)
music.load_music(music_url.replace("file:///", ""))


subtitle_window = subtitlePopup.SubtitleWindow()

def init_subtitle_window():
    subtitle_window.move_center()
    subtitle_window.protocol("WM_DELETE_WINDOW", exit)
    subtitle_window.mainloop()

def exit():
    cRED()
    print("PROGRAM CLOSED")
    cWHITE()
    
def init():
    init_subtitle_window()  
    
init()