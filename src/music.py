from mutagen.mp3 import MP3
from mutagen.m4a import M4A
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from mutagen.wavpack import WavPack
import pyglet
import os
import urllib.parse
import urllib.request
import random
from tkinter import filedialog
from src.colors import *

music_formats = [( "Music", ( "*.mp3", "*.flac", "*.wav", "*.m4a" ))]
subtitle_formats = [("Lyrics", ("*.srt", "*.lrc"))]
playlist_format = [("Playlist", ("*.m3u"))]


class MusicPlayer:
    player = pyglet.media.Player()
    playlist : list = []
    queue : list = []
    current_index : int = 0
    
    is_pause = True
    loop = True
    random = False

    data_current : pyglet.media.Source
    data_next = None
    data_previous = None
    
    def __init__(self):
        self.player.on_eos = self.on_end_song
    
    def play(self):
        self.player.queue(self.data_current)
        self.player.play()
        self.is_pause = False

    def pause(self, event = None):
        if self.player.playing: 
            self.player.pause()
            self.is_pause = True
        else:
            self.player.play()
            self.is_pause = False
    
    def add_music_list(self, list:list):
        for url in list:
            self.playlist.append(url)
            self.queue.append(url)
        self.load(True,False)
        
    def load(self, play = True, current = True):
        if self.playlist == [] : return
        if current: self.data_current = pyglet.media.load(self.queue[self.current_index], streaming=True)

        if self.current_index < len(self.queue) - 1 :
            self.data_next = pyglet.media.load(self.queue[self.current_index + 1], streaming=True)
        else :
            self.data_next = pyglet.media.load(self.queue[0], streaming=True)
        if self.current_index > 0:
            self.data_previous = pyglet.media.load(self.queue[self.current_index - 1], streaming=True)
        if self.current_index == 0:
            self.data_previous = pyglet.media.load(self.queue[-1], streaming=True)
        
        if current: self.player.seek(0)
        if play and not self.is_pause:
            self.play()


    def next(self):
        self.stop()
        if self.current_index != len(self.queue) - 1:    
            self.player.queue(self.data_next)
            self.current_index += 1
            self.load()
        elif self.current_index == len(self.queue) - 1 and self.loop:    
            self.player.queue(self.data_next)
            self.current_index = 0
            self.load()
        elif self.current_index == len(self.queue) - 1 and not self.loop:    
            self.player.queue(self.data_next)
            self.current_index = 0
            self.load(False)
               
    def back(self):
        self.stop()
        if self.current_index > 0:    
            self.player.queue(self.data_previous)
            self.current_index -= 1
        elif self.current_index == 0:    
            self.player.queue(self.data_previous)
            self.current_index = len(self.queue)-1
        self.load()

    def on_end_song(self):
        print("END_SONG()")

    def get_playback_time(self):
        if self.player.source != None:
            return self.player.time
        else:
            return 0

    def get_time_left(self):
        if self.player.source != None and self.player.playing:
            time_left = self.get_track_duration(self.queue[self.current_index]) - self.player.time
            return time_left
        else:
            return 999

    def get_track_duration(self, file:str):
        audio = None
        if file.endswith(".flac"):
            audio = FLAC(file)
        elif file.endswith(".mp3"):
            audio = MP3(file)
        elif file.endswith(".m4a"):
            audio = MP4(file)
        elif file.endswith(".wav"):
            audio = WAVE(file)
        return audio.info.length

        def open_music_files(self) -> list | None:
            urls = selectFiles()        
            return urls

    def open_music_carpet(self):
        music_folder = os.path.expanduser('~/')
        try:
            file_path = filedialog.askdirectory(title="Select a Music Carpet", initialdir=music_folder)
            carpet_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
            carpet_url = urllib.parse.unquote(carpet_url)
        except:
            print("not a carpet error")
            return None
#        with( )
        self.add_music_list()

    def stop(self):
        self.player.pause()
        self.player.delete()
        try:
            self.updater_thread.terminate()
        except AttributeError:
            pass
        self.player = pyglet.media.Player()
        self.is_pause = False

    def toggle_shuffle(self):
        self.random = not self.random
        if self.random:
            self.queue = random.shuffle(self.playlist)
            self.set_index(0)
        else:
            self.queue = self.playlist

    def get_title(self, url:str) -> str:
        if url.endswith(".mp3"):
            try: return MP3(url)["TIT1"].text[0]
            except:
                try: return MP3(url)["TIT2"].text[0]
                except:
                    try: return MP3(url)["TIT3"].text[0]
                    except: return self.get_filename(url)
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

    def set_index(self, index:int, stop = True) -> None:
        if stop: self.stop()
        self.current_index = index
        if stop: 
            self.load()
        else:
            self.load(True, False)
