import src.timeliner as timeliner
import src.subtitlePopup as subtitlePopup
import src.music as music
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
from src.colors import *


# OPENING A MUSIC FILE COMPATIBLE WITH pygame.mixer
cGREEN()
print("Please select a music file (mp3)")
cRED()
file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3"), ("FLAC", "*.flac"), ("WAVE", "*.wav"), ("M4A", "*.m4a")])
music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
music_url = urllib.parse.unquote(music_url)
music.load_music(music_url.replace("file:///", ""))

# OPENING A SRT FILE
cGREEN()
print("Please select a SRT file (subtitles file)")
cRED()
file_path = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
file_url = urllib.parse.unquote(file_url)

timeliner.srt_path = file_url


subtitle_window = subtitlePopup.SubtitleWindow()

def init_subtitle_window():
    subtitle_window.move_center()
    subtitle_window.protocol("WM_DELETE_WINDOW", exit)
    subtitle_window.mainloop()

def exit():
    cBLUE()
    print("PROGRAM CLOSED")
    cRED()
    
def init():
    init_subtitle_window()  
    
init()