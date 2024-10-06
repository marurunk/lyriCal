from src.colors import *
from src.lyric_system import LyricSystem
from src.music import MusicPlayer
from src.python_script import *
import os
import subprocess
import random

def scanPlaylist(file:str):
    parentFolder = python_script("selectFolderMusic.py")
    if parentFolder == None: return None 
    tracks = []
    with open(file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            #if the line is not a #tag continue
            if not line.startswith('#'): 
                track = parentFolder[0].strip() + "/" + line.strip()
                #if file exist add to the list
                if os.path.exists(track): tracks.append(track)
    return tracks


class Controller:
    playlist = []
    def __init__(self, GUI) -> None:
        self.GUI = GUI
        self.musicPlayer = MusicPlayer()
        self.lyricSystem = LyricSystem(self.GUI.subtitlePopup, self.musicPlayer)
    
    def load_new_song(self) -> None:
        files = python_script("selectMusic.py")
        if files == None: return
        urls = []

        for file in files:
            if file.endswith(".m3u"):
                playlist = scanPlaylist(file)
                if playlist == None: pass
                for track in playlist:
                    urls.append(track)
            else:
                urls.append(file)

        self.musicPlayer.add_music_list(urls)
        self.scan_lyrics()
        self.GUI.update_playlist()
        self.GUI.load_thread.join(10)

    
    def scan_lyrics(self):
        self.lyricSystem.playlist = []
        for url in self.musicPlayer.queue:
            self.lyricSystem.find_lyric(url)
        if not self.lyricSystem.active: self.lyricSystem.startSyncronizer()

    def load_lyric(self) -> None:
        if self.lyricSystem.active: self.lyricSystem.load_lyric()
    
    def next_song(self, e=None):
        self.musicPlayer.next()
        self.lyricSystem.next()
        pass
    
    def back_song(self, e=None):
        self.musicPlayer.back()
        self.lyricSystem.back()
        pass
    
    def delete_song(self, index : int):
        self.musicPlayer.delete_song(self.playlist[index])
        self.lyricSystem.delete_lyric(self.playlist[index])
        pass
    
    def add_song(self):
        pass

    def pause(self, e=None):
        self.musicPlayer.pause()
    
    def play(self):
        self.musicPlayer.play()
        pass

    def shuffle(self):
        titles=self.playlist 
        tracks = self.musicPlayer.queue
        lyrics = self.lyricSystem.playlist

        # SAVE CURRENT TRACK BEFORE AND DELETE IT FROM THE PLAYLISTS
        current_title = titles[self.musicPlayer.current_index]
        current_file = tracks[self.musicPlayer.current_index]
        current_lyric = lyrics[self.lyricSystem.current_index]

        titles.pop(self.musicPlayer.current_index)
        tracks.pop(self.musicPlayer.current_index)
        lyrics.pop(self.lyricSystem.current_index)
        
        # SHUFFLE 
        combine = list(zip(titles, tracks, lyrics))
        random.shuffle(combine)

        titles, tracks, lyrics = zip(*combine)

        # COMBINE AGAIN WITH FIRST CURRENT TRACK SAVED
        self.playlist = [current_title] + list(titles)
        self.musicPlayer.queue = [current_file] + list(tracks)
        self.lyricSystem.playlist = [current_lyric] + list(lyrics)

        self.musicPlayer.set_index(0, False)
        self.lyricSystem.set_index(0)
        pass

    def exit(self):
        self.GUI.animation_active = False
        cBLUE()
        print("PROGRAM CLOSED")
        cRED()
        self.lyricSystem.stopSyncronizer()
        self.musicPlayer.stop()
        self.GUI.subtitlePopup.destroy()
        self.GUI.app.destroy()

    
    def add_carpet(self):
        pass
    
    def get_titles_songs(self) -> list:
        self.playlist = []
        for music in self.musicPlayer.queue:
            title = self.musicPlayer.get_title(music)

            li = list(title)
            li.insert(0," ")
            title = "".join(li)
            self.playlist.append(title)

        return self.playlist
    
    def set_song(self, index:int) -> None:
        self.musicPlayer.set_index(index)
        self.lyricSystem.set_index(index)
