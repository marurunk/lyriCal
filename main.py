import sys
import threading
import src.timeliner as timeliner
import src.subtitlePopup as subtitlePopup
import src.music as music
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
from src.colors import *
import time

thread_list = []
subtitle_window = subtitlePopup.SubtitleWindow()

def open_music_file():
    # OPENING A MUSIC FILE COMPATIBLE WITH pyglet.media
    cGREEN()
    print("Please select a music.")
    cRED()
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3"), ("FLAC", "*.flac"), ("WAVE", "*.wav"), ("M4A", "*.m4a")])
    music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
    music_url = urllib.parse.unquote(music_url)
    music.load_music(music_url.replace("file:///", ""))

def open_subtitle_file():
    # OPENING A SRT FILE
    cGREEN()
    print("Please select a SRT file (subtitles file)")
    cRED()
    file_path = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
    file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
    file_url = urllib.parse.unquote(file_url)
    timeliner.srt_path = file_url




def init_subtitle_window():
    subtitle_window.move_center()
    subtitle_window.protocol("WM_DELETE_WINDOW", exit)
    timeliner.start(subtitle_window)
    thread_list.append(music.music_Thread)
    thread_list.append(timeliner.timeLine_thread)
    subtitle_window.mainloop()
    while music.Player.playing:
        time.sleep(0.1)
    exit()

def exit():
    cBLUE()
    timeliner.music_run = False
    music.exit()
    for thread in thread_list:
        thread.join()
    print("PROGRAM CLOSED")
    cRED()
    sys.exit()
    
def init():
    open_music_file()
    open_subtitle_file()
    init_subtitle_window()  
    
init()
