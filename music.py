import pygame
import threading

def load_music(url):
    pygame.mixer.init()
    pygame.mixer.music.load(url)
    
def play_music():
    pygame.mixer.music.play()
    
    # Espera a que el archivo de audio termine de reproducirse
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Crea un nuevo thread y ejecuta la función play_music en ese thread

musicT = threading.Thread(target=play_music)

def start():
    musicT.start()
