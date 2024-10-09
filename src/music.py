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

    # more about mutagen on: https://mutagen.readthedocs.io

class MusicPlayer:
    player = pyglet.media.Player()
    playlist : list = []
    queue : list = []
    current_index : int = 0
    
    is_pause = True
    loop = False
    random = False

    data_current : pyglet.media.Source
    data_next = None
    data_previous = None
    
    def __init__(self):
        self.player.on_eos = self.on_end_song

    def on_end_song(self, event=None):
        print("on_end_song()")
        pass
    
    def play(self):
        if self.queue == []: return    
        self.player.queue(self.data_current)
        self.player.play()
        self.is_pause = False

    def pause(self, event = None):
        if self.queue == []: return    
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
        
    def load(self, play = True, reset = True):
        if self.queue == []: return    

        if reset: self.data_current = pyglet.media.load(self.queue[self.current_index], streaming=True)

        if self.current_index < len(self.queue) - 1 :
            self.data_next = pyglet.media.load(self.queue[self.current_index + 1], streaming=True)
        else :
            self.data_next = pyglet.media.load(self.queue[0], streaming=True)
        if self.current_index > 0:
            self.data_previous = pyglet.media.load(self.queue[self.current_index - 1], streaming=True)
        if self.current_index == 0:
            self.data_previous = pyglet.media.load(self.queue[-1], streaming=True)
        
        if reset: 
            try:
                self.player.seek(0)
            except:
                pass
        if play and not self.is_pause:
            self.play()
        print("music: load() done")


    def next(self):
        if self.queue == []: return    
        self.stop()
        print("music: self.stop() done")
        if self.current_index != len(self.queue) - 1:    
            print("music: if1")
            self.player.queue(self.data_next)
            print("music: self.player.queue(self.data_next)")
            self.current_index += 1
            print("music: self.current_index += 1")
            self.load()
        elif self.current_index == len(self.queue) - 1 and self.loop:    
            print("music: elif1")
            self.player.queue(self.data_next)
            print("music: self.player.queue(self.data_next)")
            self.current_index = 0
            print("music: self.current_index = 0")
            self.load()
        elif self.current_index == len(self.queue) - 1 and not self.loop:    
            print("music: elif2")
            self.player.queue(self.data_next)
            self.current_index = 0
            self.load(False)
        print("music: next() done")
               
    def back(self):
        if self.queue == []: return    
        self.stop()
        if self.current_index > 0:    
            self.player.queue(self.data_previous)
            self.current_index -= 1
        elif self.current_index == 0:    
            self.player.queue(self.data_previous)
            self.current_index = len(self.queue)-1
        self.load()

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

    def stop(self):
        if self.queue == []: return    
        self.player.pause()
        self.player.delete()
        self.player = pyglet.media.Player()
        print("music player stop()")

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

    def get_artist(self, url:str) -> str:
        if url.endswith(".mp3"):
            try: return MP3(url)["TPE1"].text[0]
            except:
                try: return MP3(url)["TPE2"].text[0]
                except:
                    return "Unknown Artist"
        elif url.endswith(".m4a"):
            try: 
                return M4A(url)["\xa9ART"].text[0]
            except:
                try:
                    return M4A(url)["aART"].text[0]
                except:
                    return "Unknown Artist"
        elif url.endswith(".flac"):
            try:
                return FLAC(url)["artist"][0]
            except:
                    return "Unknown Artist"
        elif url.endswith(".wav"):
            try:
                return WavPack(url)["artist"][0]
            except:
                return "Unknown Artist"
        else:
            return "Unknown Artist"

    def get_album(self, url:str) -> str:
        if url.endswith(".mp3"):
            try: return MP3(url)["TALB"].text[0]
            except:
                try: return MP3(url)["TOAL"].text[0]
                except:
                    return ""
        elif url.endswith(".m4a"):
            try:
                return M4A(url)["\xa9alb"].text[0]
            except:
                return ""
        elif url.endswith(".flac"):
            try:
                return FLAC(url)["album"][0]
            except:
                return ""
        elif url.endswith(".wav"):
            try:
                return WavPack(url)["album"][0]
            except:
                return ""
        else:
            return ""

    def get_filename(self, url:str) -> str:
        name = os.path.basename(url)
        name, ext = os.path.splitext(name)
        return name

    def set_index(self, index:int, stop = True) -> None:
        if self.queue == []: return    
        if stop: self.stop()
        self.current_index = index
        if stop: 
            self.load()
        else:
            self.load(True, False)
