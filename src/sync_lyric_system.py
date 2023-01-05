import time
import tkinter
import src.music as music
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
import threading
from . import lyrics_reader
from src.colors import *

subtitle_formats = [("Lyric files", ("*.srt", "*.lrc"))]

class LyricSystem():
    def __init__(self, subtitlePopup : tkinter.Tk) -> None:
        self.current_Lyric_path : str = None
        self.current_song_title : str = None
        self.subtitlePopup : tkinter.Tk = subtitlePopup
        self.Sync_thread : threading.Thread
        self.stop_event : threading.Event = threading.Event()
        pass
    
    def change_lyric_file(self):
        self.current_Lyric_path = self.select_subtitle_file()
        self.startSyncronizer()
        
    def set_title_song(self, title:str):
        self.current_song_title = title

    def select_subtitle_file(self) -> str:
        file_path = filedialog.askopenfilename(filetypes=subtitle_formats, title="Select a Lyric file")
        file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
        file_url = urllib.parse.unquote(file_url)
        return file_url
    
    def startSyncronizer(self):
        if self.current_Lyric_path.endswith(".srt"):
            print("START SRT")
            self.syncronizer_on = True
            self.Sync_thread = threading.Thread(target=self.SRT_syncronizer_loop, args=(lyrics_reader.create_SRT_obj(self.current_Lyric_path),))
            self.Sync_thread.start()
        elif self.current_Lyric_path.endswith(".lrc"):
            print("START LRC")
            self.syncronizer_on = True
            self.Sync_thread = threading.Thread(target=self.LRC_syncronizer_loop, args=(lyrics_reader.create_LRC_object(self.current_Lyric_path),))
            self.Sync_thread.start()

    def stopSyncronizer(self):
        print("Stop Syncronizer")
        self.stop_event.set()

    def SRT_syncronizer_loop(self, SRT_object : lyrics_reader.SRT_Object):
        
        times_list = []
        for itime in SRT_object.times:
            times_list.append(itime["start"])
            times_list.append(itime["end"])

        while not self.stop_event.is_set():
            subtitle_index = -1

            for i, subtitle_time in enumerate(times_list):
                if music.reproductor.get_playback_time() > subtitle_time:
                    subtitle_index = i
                else:
                    break

            if subtitle_index != -1 and subtitle_index % 2 == 0:
                subtitle = SRT_object.subtitles[int(subtitle_index/2)]
                self.subtitlePopup.set_txt(subtitle)
            else:
                self.subtitlePopup.set_txt("")
            time.sleep(0.001)

    def LRC_syncronizer_loop(self, LRC_object: lyrics_reader.LRC_Object):
        while not self.stop_event.is_set():
            subtitle_index = -1

            for i, LyricObj in enumerate(LRC_object.lyricsList):
                if music.reproductor.get_playback_time() > LyricObj["time"]:
                    subtitle_index = i
                else:
                    break

            if subtitle_index != -1:
                subtitle = LRC_object.lyricsList[subtitle_index]["lyric"]
                try:
                    self.subtitlePopup.set_txt(subtitle)
                except RuntimeError:
                    print("RUNTIME ERROR")
            else:
                try:
                    self.subtitlePopup.set_txt("")
                except RuntimeError:
                    print("RUNTIME ERROR")

            time.sleep(0.001)

