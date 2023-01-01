import time
import src.music as music
from datetime import datetime, timedelta
import threading
import src.srt_class as srt_class
from src.colors import *

srt_path = ""

mySRT:srt_class.Class_SRT = None

music_run = False


def start_timeliner(subTk):
    #print("start_timeliner()")
    indice = 0
    indice2 = 0
    
    # Iniciamos el contador
    inicio = datetime.now()
    
    tiempos = []
    for itime in mySRT.times:
        tiempos.append(itime["start"])
        tiempos.append(itime["end"])
    
    while indice < len(tiempos) and music_run == True:
        # Convertimos el tiempo actual a milisegundos
        tiempo_ms = timedelta(hours=int(tiempos[indice][:2]), minutes=int(tiempos[indice][3:5]), seconds=int(tiempos[indice][6:8]), milliseconds=int(tiempos[indice][9:])).total_seconds() * 1000


        # Comprobamos cada milisegundo si el siguiente tiempo ya llegó
        # while (datetime.now() - inicio).total_seconds() * 1000 < tiempo_ms:
        while music.get_playback_time() * 1000 < tiempo_ms and music_run == True:
            time.sleep(0.001)

        if indice % 2 != 0:
            subTk.set_txt("")
        else:
            subTk.set_txt(mySRT.subtitles[indice2])
            indice2 += 1
        # Avanzamos al siguiente tiempo
        indice += 1

#    print("No pos termino este proceso de timeline")        
    
def start(subTk):
    global mySRT, timeLine_thread, music_run
    mySRT = srt_class.Class_SRT(srt_class.create_dict(srt_path))
    timeLine_thread = threading.Thread(target=start_timeliner, args=(subTk,))
    music_run = True
    music.start()
    timeLine_thread.start()
