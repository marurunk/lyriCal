from src.colors import *
from src.lyric_system import LyricSystem
from src.music import MusicPlayer
from src.python_script import *
from src.notify import *
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
    titles = []
    artists = []
    albums = []
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
        self.scan_titles()
        self.scan_artists()
        self.scan_albums()
        self.GUI.update_playlist()
    
    def scan_lyrics(self):
        self.lyricSystem.playlist = []
        for url in self.musicPlayer.queue:
            self.lyricSystem.find_lyric(url)

    def load_lyric(self) -> None:
        if self.lyricSystem.active: self.lyricSystem.load_lyric()
    
    def next_song(self, e=None):
        if not self.lyricSystem.active: self.lyricSystem.startSyncronizer()
        self.musicPlayer.next()
        self.lyricSystem.next()
        self.notify_song()
    
    def back_song(self, e=None):
        if not self.lyricSystem.active: self.lyricSystem.startSyncronizer()
        self.musicPlayer.back()
        self.lyricSystem.back()
        self.notify_song()

    def set_song(self, index:int) -> None:
        if not self.lyricSystem.active: self.lyricSystem.startSyncronizer()
        self.musicPlayer.set_index(index)
        self.lyricSystem.set_index(index)
        self.musicPlayer.play()
        self.notify_song()
    
    def delete_song(self, index : int):
        self.musicPlayer.delete_song(index)
        self.lyricSystem.delete_lyric(index)
        pass
    
    def add_song(self):
        pass

    def pause(self, e=None):
        self.musicPlayer.pause()
    
    def play(self):
        if not self.lyricSystem.active: self.lyricSystem.startSyncronizer()
        self.musicPlayer.play()

    def toggle_loop(self):
        self.musicPlayer.loop = not self.musicPlayer.loop
        self.lyricSystem.loop = not self.lyricSystem.loop

    def toggle_random(self):
        # work in progresss
        self.shuffle()

    def shuffle(self):
        if self.titles == []: return 
        titles=self.titles 
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
        self.titles = [current_title] + list(titles)
        self.musicPlayer.queue = [current_file] + list(tracks)
        self.lyricSystem.playlist = [current_lyric] + list(lyrics)

        self.musicPlayer.set_index(0, False)
        self.lyricSystem.set_index(0)
        pass

    def exit(self):
        cBLUE()
        print("exiting..")
        cRED()
        self.lyricSystem.stopSyncronizer()
        self.musicPlayer.stop()
        self.GUI.subtitlePopup.exit()

    
    def add_carpet(self):
        pass
    
    def scan_titles(self) -> list:
        if self.musicPlayer.queue == []: return    
        self.titles = []
        for music in self.musicPlayer.queue:
            title = self.musicPlayer.get_title(music)
            self.titles.append(title)

    def scan_artists(self) -> list:
        if self.musicPlayer.queue == []: return    
        self.artists = []
        for music in self.musicPlayer.queue:
            artist = self.musicPlayer.get_artist(music)
            self.artists.append(artist)

    def scan_albums(self) -> list:
        if self.musicPlayer.queue == []: return    
        self.albums = []
        for music in self.musicPlayer.queue:
            album = self.musicPlayer.get_album(music)
            self.albums.append(album)
    

    def notify_song(self):
        if self.musicPlayer.queue == []: return    
        notify(
                self.titles[self.musicPlayer.current_index], 
                "by " + self.artists[self.musicPlayer.current_index])
