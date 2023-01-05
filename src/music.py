import pyglet
import os
import urllib.parse
import urllib.request
from tkinter import filedialog
from src import timeliner
from src.colors import *

music_formats = [("MP3 Files", "*.mp3"), ("FLAC", "*.flac"), ("WAVE", "*.wav"), ("M4A", "*.m4a")]
subtitle_formats = [("SRT files", "*.srt")]



class MusicPlayer:
    player = pyglet.media.Player()
    playlist : list = []
    current_index : int = 0

    data_current = None
    data_next = None
    data_previous = None
    
    def play(self):
        self.player.play()
        print("Play()")

    def pause(self):
        print("pause()")
        if self.player.playing: 
            self.player.pause()
        else:
            self.player.play()
    
    def add_music_list(self, list:list):
        print("lista :", list)
        for url in list:
            self.playlist.append(url)
        self.load()
        self.player.queue(self.data_current)
    
    def load(self):
        print("load")
        if len(self.playlist) != 0 :
            self.data_current = pyglet.media.load(self.playlist[self.current_index])

        if len(self.playlist) > 1 and self.current_index < len(self.playlist) - 1:
            self.data_next = pyglet.media.load(self.playlist[self.current_index + 1])
        if self.current_index > 0:
            self.data_previous = pyglet.media.load(self.playlist[self.current_index - 1])

    def next(self):
        self.player.delete()
        self.player.queue(self.data_next)
        self.play()
        self.current_index += 1
        self.load()
 
    def previous(self):
        self.player.delete()
        self.player.queue(self.data_previous)
        self.play()
        self.current_index -= 1
        self.load()
    
    def get_playback_time(self):
        return self.player.time

    def open_music_file(self):
        # OPENING A MUSIC FILE COMPATIBLE WITH pyglet.media
        cGREEN()
        print("Please select a music.")
        cRED()
        file_path = filedialog.askopenfilename(filetypes=music_formats)
        music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
        music_url = urllib.parse.unquote(music_url)
        self.add_music_list([music_url.replace("file:///", "")])

    def open_music_carpet(self):
        # OPENING A MUSIC FILE COMPATIBLE WITH pyglet.media
        cGREEN()
        print("Please select a music carpet.")
        cRED()
        try:
            file_path = filedialog.askdirectory()
            music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
            music_url = urllib.parse.unquote(music_url)
        except:
            print("not a carpet error")
            return
        # self.add_music_list([music_url.replace("file:///", "")])

    def open_subtitle_file():
        # OPENING A SRT FILE
        cGREEN()
        print("Please select a SRT file (subtitles file)")
        cRED()
        file_path = filedialog.askopenfilename(filetypes=subtitle_formats)
        file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
        file_url = urllib.parse.unquote(file_url)
        timeliner.srt_path = file_url

    def exit(self):
        self.player.pause()
        self.player.delete()

reproductor = MusicPlayer()




