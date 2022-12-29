import threading
import pyglet

song = None

def load_music(url):
    global song
    song = pyglet.media.load(url)
    
    
def play_music():
    song.play()
    pyglet.app.run()

musicT = threading.Thread(target=play_music)

def start():
    musicT.start()
