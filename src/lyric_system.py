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
        self.is_active = threading.Event()
        self.loop = True
        self.lock = threading.Lock()

    def set_current_lyric(self, index : int) -> None:
        self.current_Lyric_path = self.playlist_lyrics_path[index]

    
    def load_lyric(self) -> None:
        if self.playlist == []: return
        try: file_path = filedialog.askopenfilename(filetypes=subtitle_formats, title="Select a Lyric file")
        except: 
            self.current_Lyric_path = None
            self.add_lyric_path(file_url)
        finally:
            file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
            file_url = urllib.parse.unquote(file_url)
            
            self.playlist[self.current_index] = file_url
            self.current_Lyric_path = file_url
            
    
    def find_lyric(self, url : str) -> bool: # BUG THREAD CONFLICT
        self.stopSyncronizer()
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

    def delete_lyric_path(self, URL : str) -> None:
        self.playlist_lyrics_path.remove(URL)

    def stopSyncronizer(self) -> None:
        with self.lock:
            self.is_active.clear()
            self.is_active = threading.Event()
            self.subtitlePopup.unshow()
        
    def SRT_syncronizer_loop(self, SRT_object : lyrics_reader.SRT_Object) -> None:
        times_list = []
        for both_times in SRT_object.times:
            times_list.append(both_times["start"])
            times_list.append(both_times["end"])

        # while self.is_active:
        while self.is_active.is_set():
            subtitle_index = -1
            for i, subtitle_time in enumerate(times_list):
                if not self.is_active.is_set():
                    subtitle_index = -2
                    break
                if self.musicPlayer.get_playback_time() > subtitle_time:
                    subtitle_index = i
                else:
                    break
            
            if subtitle_index == -2: break
            
            if subtitle_index != -1 and subtitle_index % 2 == 0:
                subtitle = SRT_object.subtitles[int(subtitle_index/2)]
                try: self.subtitlePopup.set_txt(subtitle)
                except RuntimeError: print("RUNTIME ERROR")
            else:
                try: self.subtitlePopup.set_txt("")
                except RuntimeError: print("RUNTIME ERROR")
            time.sleep(0.001)
        print("SRT thread: BUCLE CERRADO")

    def LRC_syncronizer_loop(self, LRC_object : lyrics_reader.LRC_Object) -> None:
        # while self.is_active:
        while self.is_active.is_set():
            subtitle_index = -1
            with self.lock:
                if not self.is_active.is_set():
                    break

            for i, LyricObj in enumerate(LRC_object.lyricsList):
                with self.lock:
                    if not self.is_active.is_set():
                        subtitle_index = -2
                        break
                
                if self.musicPlayer.get_playback_time() > LyricObj["time"]:
                    subtitle_index = i
                else:
                    break
            if subtitle_index == -2: break

            if subtitle_index != -1:
                subtitle = LRC_object.lyricsList[subtitle_index]["lyric"]
                try: self.subtitlePopup.app.after(1,self.subtitlePopup.set_txt(subtitle))
                except RuntimeError: print("RUNTIME ERROR")
            else:
                try: self.subtitlePopup.app.after(1,self.subtitlePopup.set_txt(""))
                except RuntimeError: print("RUNTIME ERROR")

            time.sleep(0.001)
        print("LRC thread: BUCLE CERRADO")
    
    def startSyncronizer(self) -> None:
        with self.lock:
            if self.is_active.is_set(): raise RuntimeError
        if self.current_Lyric_path == None: return
        self.subtitlePopup.show()
        if self.current_Lyric_path.endswith(".srt"):
            print("START SRT")
            SRT = lyrics_reader.create_SRT_obj(self.current_Lyric_path)
            syncronizer_SRT_thread = threading.Thread( 
                                            target=self.SRT_syncronizer_loop, 
                                            args=(SRT,))
            self.is_active.set()
            syncronizer_SRT_thread.start()
        elif self.current_Lyric_path.endswith(".lrc"):
            print("START LRC")
            LRC = lyrics_reader.create_LRC_object(self.current_Lyric_path)
            syncronizer_LRC_thread = threading.Thread(
                                            target=self.LRC_syncronizer_loop, 
                                            args=(LRC,))
            self.is_active.set()
            # self.is_active = True
            syncronizer_LRC_thread.start()

    def next(self):
        self.stopSyncronizer()
        if self.playlist == [] : return
        if self.current_index < len(self.playlist) - 1:    
            self.current_Lyric_path = self.playlist[self.current_index + 1]
            self.current_index += 1
        elif self.current_index == len(self.playlist) - 1 and self.loop:    
            self.current_Lyric_path = self.playlist[0]
            self.current_index = 0

        self.startSyncronizer()
               
    def back(self):
        self.stopSyncronizer()
        if self.playlist == [] : return
        if self.current_index > 0:    
            self.current_Lyric_path = self.playlist[self.current_index - 1]
            self.current_index -= 1
        elif self.current_index == 0 and self.loop:
            self.current_Lyric_path = self.playlist[-1]
            self.current_index = len(self.playlist) - 1
            
            self.current_index = len(self.playlist)-1
        self.startSyncronizer()

    def set_index(self, index:int) -> None:
        self.stopSyncronizer()
        self.current_index = index
        self.current_Lyric_path = self.playlist[self.current_index]
        self.startSyncronizer()
