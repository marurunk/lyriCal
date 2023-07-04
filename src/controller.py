from src.colors import *
from src.lyric_system import LyricSystem
from src.music import MusicPlayer
import os
import subprocess

selecfile_path = os.path.abspath(__file__)
selecfile_path = os.path.dirname(selecfile_path)
selecfile_path = os.path.join(selecfile_path, "selectFile.py")

def get_files(script_path) -> list | None:
    proceso = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proceso.communicate()
    if proceso.returncode == 0:
        archivos_seleccionados = stdout.decode().splitlines()
        print("archivos seleccionados::")
        print(archivos_seleccionados)

    proceso.kill()
    if archivos_seleccionados[0] == "None" or archivos_seleccionados == None: return None
    else:
        return archivos_seleccionados



class Controller:
    def __init__(self, GUI) -> None:
        self.GUI = GUI
        self.musicPlayer = MusicPlayer()
        self.lyricSystem = LyricSystem(self.GUI.subtitlePopup, self.musicPlayer)
        self.playlist = []
    
    def load_new_song(self) -> None:

        # urls = self.musicPlayer.open_music_files()
        urls = get_files(selecfile_path)
        if urls == None: return
        self.musicPlayer.add_music_list(urls)
        for url in urls:
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
