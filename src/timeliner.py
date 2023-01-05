import time
import src.music as music
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
from datetime import datetime, timedelta
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
    # index = 0
    # sub_index = 0
        
    # unimos todos los tiempos en una lista
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

        print("subtitle_index = ", subtitle_index)
        if subtitle_index != -1 and subtitle_index % 2 == 0:
            subtitle = mySRT.subtitles[int(subtitle_index/2)]
            subTk.set_txt(subtitle)
        else:
            subTk.set_txt("")

        time.sleep(0.001)
    
    # while index < len(times_list) and music_run == True:
    #     # Convertimos el tiempo actual a milisegundos
    #     # time_ms = timedelta(hours=int(times_list[index][:2]), minutes=int(times_list[index][3:5]), seconds=int(times_list[index][6:8]), milliseconds=int(times_list[index][9:])).total_seconds() * 1000
    #     time_ms = times_list[index]


    #     # Comprobamos cada milisegundo si el siguiente tiempo ya llegó
    #     while music.reproductor.get_playback_time() < time_ms and music_run == True:
    #         time.sleep(0.001)

    #     # if index is impar subtitle text is nothing
    #     if index % 2 != 0:
    #         subTk.set_txt("")
        
    #     # else set the subtitle text by index
    #     else:
    #         subTk.set_txt(mySRT.subtitles[sub_index])
    #         sub_index += 1
    #     # Avanzamos al siguiente tiempo
    #     index += 1

    
def start(subTk):
    global mySRT, timeLine_thread, music_run
    mySRT = srt_class.Class_SRT(srt_class.create_dict(srt_path))
    timeLine_thread = threading.Thread(target=start_timeliner, args=(subTk,))
    music_run = True
    #music.start()
    music.reproductor.play()
    timeLine_thread.start()
