import sys
from src import timeliner
from src import subtitlePopup
from src import music
from src.colors import *

subtitle_window = subtitlePopup.SubtitleWindow()

def init_subtitle_window():
    subtitle_window.move_center()
    subtitle_window.protocol("WM_DELETE_WINDOW", exit)
    timeliner.start(subtitle_window)

    #thread_list.append(music.music_Thread)
    thread_list.append(timeliner.timeLine_thread)
    subtitle_window.mainloop()
    exit()

def exit():
    cBLUE()
    timeliner.music_run = False
    music.reproductor.exit()
    print("PROGRAM CLOSED")
    cRED()
    sys.exit()

def init():
    # music.reproductor.open_music_carpet()
    music.reproductor.open_music_file()
    timeliner.open_subtitle_file()
    init_subtitle_window()



init()
