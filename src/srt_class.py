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

  for resultado in get_times(file):
      start, end = resultado
      dict["times"].append({"start":start, "end": end})
  return dict
      
class Class_SRT:
  def __init__(self, data:dict) -> None:
    self.subtitles = data["subtitles"]
    self.times = data["times"]





