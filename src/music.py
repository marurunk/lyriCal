from mutagen.mp3 import MP3
from mutagen.m4a import M4A
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.wavpack import WavPack
import pyglet
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
from src.colors import *

music_formats = [( "Music Files", ( "*.mp3", "*.flac", "*.wav", "*.m4a" ))]
subtitle_formats = [("SRT files", "*.srt")]

class MusicPlayer:
    player = pyglet.media.Player()
    playlist : list = []
    current_index : int = 0
    
    loop = True

    data_current : pyglet.media.Source
    data_next = None
    data_previous = None
    
    def __init__(self):
        self.player.on_eos = self.on_end_song
    
    def play(self):
        self.player.queue(self.data_current)
        self.player.play()
        print(f"MusicPlayer: {self.current_index+1}/{len(self.playlist)} | {os.path.basename(self.playlist[self.current_index])}")

    def pause(self, event = None):
        if self.player.playing: 
            self.player.pause()
        else:
            self.player.play()
    
    def add_music_list(self, list:list):
        for url in list:
            self.playlist.append(url)
        self.load()
        
    def load(self):
        if self.playlist == [] : return
        
        self.data_current = pyglet.media.load(self.playlist[self.current_index], streaming=True)

        if self.current_index < len(self.playlist) - 1 :
            self.data_next = pyglet.media.load(self.playlist[self.current_index + 1], streaming=True)
        else :
            self.data_next = pyglet.media.load(self.playlist[0], streaming=True)
        if self.current_index > 0:
            self.data_previous = pyglet.media.load(self.playlist[self.current_index - 1], streaming=True)
        if self.current_index == 0:
            self.data_previous = pyglet.media.load(self.playlist[-1], streaming=True)

    def next(self):
        self.stop()
        if self.current_index != len(self.playlist) - 1:    
            self.player.queue(self.data_next)
            self.current_index += 1
        elif self.current_index == len(self.playlist) - 1 and self.loop:    
            self.player.queue(self.data_next)
            self.current_index = 0
        self.load()
        self.player.seek(0)
        self.play()
               
    def back(self):
        self.stop()
        if self.current_index > 0:    
            self.player.queue(self.data_previous)
            self.current_index -= 1
        elif self.current_index == 0 and self.loop:    
            self.player.queue(self.data_previous)
            self.current_index = len(self.playlist)-1
        self.load()
        self.player.seek(0)
        self.play()

    def on_end_song(self):
        print("END_SONG()")

    def get_playback_time(self):
        if self.player.source != None:
            return self.player.time
        else:
            return 0

    def open_music_file(self) -> str | None:
        music_folder = os.path.expanduser('~/Music')
        file_path = filedialog.askopenfilename(filetypes=music_formats, title="Select a Music file", initialdir=music_folder)
        if file_path == "": return None
        music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
        music_url = urllib.parse.unquote(music_url)
        self.add_music_list([music_url.replace("file:///", "")])
        return music_url.replace("file:///", "")

    def open_music_carpet(self):
        music_folder = os.path.expanduser('~/Music')
        try:
            file_path = filedialog.askdirectory(title="Select a Music Carpet", initialdir=music_folder)
            music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
            music_url = urllib.parse.unquote(music_url)
        except:
            print("not a carpet error")
            return
        # self.add_music_list([music_url.replace("file:///", "")])

    def stop(self):
        self.player.pause()
        self.player.delete()
        try:
            self.updater_thread.terminate()
        except AttributeError:
            pass
        self.player = pyglet.media.Player()

    def get_title(self, url:str) -> str:
        if url.endswith(".mp3"):
            try: return MP3(url)["TIT1"].text[0]
            except KeyError:
                try: return MP3(url)["TIT2"].text[0]
                except KeyError:
                    try: return MP3(url)["TIT3"].text[0]
                    except KeyError: return self.get_filename(url)
        elif url.endswith(".m4a"):
            return M4A(url)["\xa9nam"].text[0]
        elif url.endswith(".flac"):
            return FLAC(url)["title"][0]
        elif url.endswith(".wav"):
            return WavPack(url)["title"][0]
        else:
            return "ERROR"

    def get_filename(self, url:str) -> str:
        name = os.path.basename(url)
        name, ext = os.path.splitext(name)
        return name

    def set_index(self, index:int) -> None:
        self.stop()
        self.current_index = index
        self.load()
        self.play()
