import sys
from src import sync_lyric_system
from src import subtitlePopup
from src import music
from src.colors import *

subtitlePopup = subtitlePopup.SubtitleWindow()
lyricSystem = sync_lyric_system.LyricSystem(subtitlePopup)

def init_subtitle_window():
    subtitlePopup.move_center()
    subtitlePopup.protocol("WM_DELETE_WINDOW", exit)

    subtitlePopup.mainloop()
    exit()

def exit():
    cBLUE()
    lyricSystem.stopSyncronizer()
    music.reproductor.exit()
    print("PROGRAM CLOSED")
    cRED()
    sys.exit()

def init():
    # music.reproductor.open_music_carpet()
    music.reproductor.open_music_file()
    
    lyricSystem.change_lyric_file()
    music.reproductor.play()
    init_subtitle_window()  



init()