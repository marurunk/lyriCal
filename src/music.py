import threading
import pyglet
import time

def load_music(url):
    global Player, song

    Player = pyglet.media.Player()
    song = pyglet.media.load(url, streaming=False)
    Player.queue(song)
    Player.loop = True
   
def get_playback_time()-> float:
    return Player.time # TIME IN SECONDS | FLOAT
 
def play_music():
    Player.play()
 
def exit():
    Player.pause()
    Player.delete()
    
music_Thread = threading.Thread(target=play_music)

def start():
    music_Thread.start()
