import time
import tkinter
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
import threading
from src import lyrics_reader
from src.colors import *
from src.subtitlePopup import SubtitlePopup

subtitle_formats = [("Lyric files", ("*.srt", "*.lrc"))]

class LyricSystem():
    def __init__(self, subtitlePopup:tkinter.Toplevel, musicPlayer: SubtitlePopup) -> None:
        self.playlist = []
        self.current_Lyric_path : str = None
        self.current_index = 0
        self.subtitlePopup = subtitlePopup
        self.musicPlayer = musicPlayer
        self.loop = True
        self.main_thread : threading.Thread
        self.current_LyricObjet : lyrics_reader.LyricObject
        self.active = False
        self.lock = threading.Lock()    

    def set_current_lyric(self, index : int) -> None:
        self.current_index = index
        self.change_lyric()

    
    def load_lyric(self) -> None:
        if self.playlist == []: return
        file_path = filedialog.askopenfilename(filetypes=subtitle_formats, title="Select a Lyric file")
        if file_path == None:
            print("file path is none")
            self.current_Lyric_path = None
            self.add_lyric_path(None)
            return
        else:
            file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
            file_url = urllib.parse.unquote(file_url)
            
            print(f"file path is {file_url}")
            self.current_Lyric_path = file_url
            self.playlist[self.current_index] = file_url
            self.add_lyric_path(self.current_Lyric_path)
    
    def find_lyric(self, url : str) -> bool:
        carpet = os.path.dirname(url)
        file_list = os.listdir(carpet)
        song_name = os.path.basename(url)
        song_name, ext = os.path.splitext(song_name)
        for file in file_list:
            name , extention = os.path.splitext(file)
            if name == song_name and extention in [".lrc",".srt"]:
                self.current_Lyric_path = carpet + "/" + file 
                self.add_lyric_path(self.current_Lyric_path)
                return True
        
        self.add_lyric_path(None)
        return False

    def add_lyric_path(self, URL : str | None) -> None:
        self.playlist.append(URL)
        self.current_index = len(self.playlist)-1
        self.change_lyric()

    def delete_lyric_path(self, URL : str) -> None:
        self.playlist.remove(URL)

    def stopSyncronizer(self) -> None:
        self.active = False
        self.subtitlePopup.unshow()
        try: self.main_thread.join(10)
        except AttributeError: pass
        
    def startSyncronizer(self) -> None:
        self.subtitlePopup.show()
        self.main_thread = threading.Thread(target=self.sync_loop)
        self.active = True
        self.main_thread.start()

    def next(self):
        if self.playlist == [] : return
        if self.current_index < len(self.playlist) - 1:    
            self.current_index += 1
            self.change_lyric()
        elif self.current_index == len(self.playlist) - 1 and self.loop:    
            self.current_index = 0
            self.change_lyric()
               
    def back(self):
        if self.playlist == [] : return
        if self.current_index > 0:    
            self.current_index -= 1
            self.change_lyric()
        elif self.current_index == 0 and self.loop:
            self.current_index = len(self.playlist) - 1
            self.change_lyric()

    def set_index(self, index:int) -> None:
        self.current_index = index
        self.change_lyric()
        
    def change_lyric(self):
        self.current_Lyric_path = self.playlist[self.current_index]
        if not self.current_Lyric_path == None:
            with self.lock:
                self.current_LyricObjet = lyrics_reader.LyricObject(self.current_Lyric_path)
        else:
            self.current_LyricObjet = None
            
    def sync_loop(self):
        print("sync loop start")
        self.subtitlePopup.show()
        while self.active:
            if self.current_LyricObjet == None:
                self.subtitlePopup.unshow()
                time.sleep(1)
                continue
            if self.current_LyricObjet.format == "LRC":
                self.subtitlePopup.show()
                self.LRC_syncronizer(self.current_LyricObjet)
            elif self.current_LyricObjet.format == "SRT":
                self.subtitlePopup.show()
                self.SRT_syncronizer(self.current_LyricObjet)
            
            time.sleep(0.2)
        print("sync loop end")
    
    def SRT_syncronizer(self,SRT_object) -> None:
        times_list = []
        try:
            for both_times in SRT_object.times:
                times_list.append(both_times["start"])
                times_list.append(both_times["end"])
        except AttributeError: return
        subtitle_index = -1
        for i, subtitle_time in enumerate(times_list):
            if self.musicPlayer.get_playback_time() > subtitle_time: subtitle_index = i
            else: break
        
        if subtitle_index != -1 and subtitle_index % 2 == 0:
            subtitle = SRT_object.subtitles[int(subtitle_index/2)]
            try: self.subtitlePopup.set_txt(subtitle)
            except RuntimeError: return
        else:
            try: self.subtitlePopup.set_txt("")
            except RuntimeError: return

    def LRC_syncronizer(self,LRC_object) -> None:
        subtitle_index = -1
        try:
            for i, LyricObj in enumerate(LRC_object.lyricsList):
                if self.musicPlayer.get_playback_time() > LyricObj["time"]:
                    subtitle_index = i
                else:
                    break
        except AttributeError: return
        
        if subtitle_index != -1:
            subtitle = LRC_object.lyricsList[subtitle_index]["lyric"]
            try: self.subtitlePopup.app.after(1, self.subtitlePopup.set_txt(subtitle))
            except RuntimeError: return
        else:
            try: self.subtitlePopup.app.after(1, self.subtitlePopup.set_txt(""))
            except RuntimeError: return
