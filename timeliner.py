import time
import music
from datetime import datetime, timedelta
import threading
import srt_class
from colors import *

ruta_srt = ""

mySRT:srt_class.Class_SRT = None



def start_timeliner(subTk):
    # Índice del tiempo actual
    indice = 0
    indice2 = 0
    print(mySRT.times)
    inicio = datetime.now()
    
    tiempos = []
    for itime in mySRT.times:
        tiempos.append(itime["start"])
        tiempos.append(itime["end"])
    
    while indice < len(tiempos):
        # Convertimos el tiempo actual a milisegundos
        tiempo_ms = timedelta(hours=int(tiempos[indice][:2]), minutes=int(tiempos[indice][3:5]), seconds=int(tiempos[indice][6:8]), milliseconds=int(tiempos[indice][9:])).total_seconds() * 1000

        # Iniciamos el contador

        # Comprobamos cada milisegundo si el siguiente tiempo ya llegó
        while (datetime.now() - inicio).total_seconds() * 1000 < tiempo_ms:
            time.sleep(0.001)

        # Si llegamos aquí es porque el tiempo actual ha pasado
        # Podemos hacer algo aquí, como imprimir un mensaje o llamar a otra función
        print("Ha pasado el tiempo", tiempos[indice])
        if indice % 2 != 0:
            subTk.set_txt("")
        else:
            subTk.set_txt(mySRT.subtitles[indice2])
            indice2 += 1
        # Avanzamos al siguiente tiempo
        indice += 1

        
    
def start(subTk):
    global mySRT
    mySRT = srt_class.Class_SRT(srt_class.create_dict(ruta_srt))
    cBlue()
    print("LECTOR SRT START()")
    timeLine_thread = threading.Thread(target=start_timeliner, args=(subTk,))
    timeLine_thread.start()
    music.start()