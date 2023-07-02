from src.colors import *
from src.lyric_system import LyricSystem
from src.music import MusicPlayer


class Controller:
    def __init__(self, GUI) -> None:
        self.GUI = GUI
        self.musicPlayer = MusicPlayer()
        self.lyricSystem = LyricSystem(self.GUI.subtitlePopup, self.musicPlayer)
        self.playlist = []
    
    def load_new_song(self) -> None:
        url = self.musicPlayer.open_music_file()
        if url == None: return
        if self.lyricSystem.find_lyric(url):
            pass
        title = self.musicPlayer.get_title(url)
        cRED()
        print("the title is ::: ", title)
        cWHITE()
        li = list(title)
        li.insert(0," ")
        title = "".join(li)
        self.playlist.append(title)
        if not self.lyricSystem.active: self.lyricSystem.startSyncronizer()
    
    def load_lyric(self) -> None:
        if not self.lyricSystem.active: return
        self.lyricSystem.load_lyric()
    
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
        return self.playlist
    
    def set_song(self, index:int) -> None:
        self.musicPlayer.set_index(index)
        self.lyricSystem.set_index(index)
