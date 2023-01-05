from datetime import timedelta
import re

musicURL = "myMusic.srt"
patron_txt = r"\d+\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\n((?:.|\n)*?)(?=\n\d+\n|$)"
patron_times = r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)"

def read(file:str):
  # Leer el archivo srt
  with open(file.replace("file:///",""), "r", encoding="utf-8") as f:
      return f.read()
    
def get_subs(file:str):
    # Obtener dialogos
    subs = re.findall(patron_txt, read(file))
    for i, sub in enumerate(subs):
        # Eliminamos el salto de línea final de la cadena de texto
        sub_modified = sub.rstrip()
        # Reasignamos el valor modificado a la variable original
        subs[i] = sub_modified
    
    return subs

def get_times(file:str):
  # Obtener tiemposd (start, end)
  return re.findall(patron_times, read(file))

def create_dict(file:str):
  dict = {
    "subtitles": get_subs(file),
    "times": []
  }

  for time in get_times(file):
      start, end = time
      # parse text to seconds
      start = timedelta(hours=int(start[:2]), minutes=int(start[3:5]), seconds=int(start[6:8]), milliseconds=int(start[9:])).total_seconds()
      end = timedelta(hours=int(end[:2]), minutes=int(end[3:5]), seconds=int(end[6:8]), milliseconds=int(end[9:])).total_seconds()

      
      dict["times"].append({"start":start, "end": end})
  return dict
      
class Class_SRT:
  def __init__(self, data:dict) -> None:
    self.subtitles = data["subtitles"]
    self.times = data["times"]





