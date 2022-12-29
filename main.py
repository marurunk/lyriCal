import timeliner
from tkinter import filedialog
import subtitulo
from colors import *
import music
import os
import urllib.parse
import urllib.request

file_path = filedialog.askopenfilename()
file_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
file_url = urllib.parse.unquote(file_url)

print(file_url)
timeliner.ruta_srt = file_url

file_path = filedialog.askopenfilename()
music_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(os.path.abspath(file_path)))
music_url = urllib.parse.unquote(music_url)
music.load_music(music_url.replace("file:///", ""))


ventana = subtitulo.LyricPopup()

def mostrar_ventana():
    ventana.move_center()
    ventana.protocol("WM_DELETE_WINDOW", exit)
    ventana.mainloop()

def exit():
    cRed()
    print("PROGRAMA CERRADO")
    
def init():
    mostrar_ventana()  
    
init()