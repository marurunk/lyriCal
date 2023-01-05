import time
import src.music as music
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
import threading
from src import srt_class
from src.colors import *

srt_path = ""

mySRT:srt_class.Class_SRT = None

music_run = False

subtitle_formats = [("SRT files", "*.srt")]


def open_subtitle_file():
    global srt_path
    # OPENING A SRT FILE
    cGREEN()
    print("Please select a SRT file (subtitles file)")
    cRED()
    file_path = filedialog.askopenfilename(filetypes=subtitle_formats)
    file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
    file_url = urllib.parse.unquote(file_url)
    srt_path = file_url


def start_timeliner(subTk):
    
    times_list = []
    for itime in mySRT.times:
        times_list.append(itime["start"])
        times_list.append(itime["end"])

    while music_run == True:
        subtitle_index = -1

        for i, subtitle_time in enumerate(times_list):
            if music.reproductor.get_playback_time() > subtitle_time:
                subtitle_index = i
            else:
                break

        if subtitle_index != -1 and subtitle_index % 2 == 0:
            subtitle = mySRT.subtitles[int(subtitle_index/2)]
            subTk.set_txt(subtitle)
        else:
            subTk.set_txt("")

        time.sleep(0.001)
    
    
def start(subTk):
    global mySRT, timeLine_thread, music_run
    mySRT = srt_class.Class_SRT(srt_class.create_dict(srt_path))
    timeLine_thread = threading.Thread(target=start_timeliner, args=(subTk,))
    
    music_run = True
    music.reproductor.play()
    timeLine_thread.start()
