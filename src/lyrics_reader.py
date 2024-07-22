from datetime import timedelta
import re
import os

patron_SRT_text = r"\d+\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\n((?:.|\n)*?)(?=\n\d+\n|$)"
patron_SRT_times = r"(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)"
patron_LRC_time = r'\[(\d+):(\d+)\]'

def read_lyric_file(file_URL:str) -> str:
    if os.name == "nt":
        with open(file_URL.replace("file:///",""), "r", encoding="utf-8") as f:
            return f.read()
    if os.name == "posix":
        with open(file_URL.replace("file:///","/"), "r", encoding="utf-8") as f:
            return f.read()
def get_SRT_subs(file_URL:str) -> list:
    # Obtener dialogos
    subs = re.findall(patron_SRT_text, read_lyric_file(file_URL))
    for i, sub in enumerate(subs):
        # Eliminamos el salto de línea final de la cadena de texto
        sub_modified = sub.rstrip()
        # Reasignamos el valor modificado a la variable original
        subs[i] = sub_modified
    
    return subs

def get_SRT_times(file_URL:str):
  # Obtener tiemposd (start, end)
  return re.findall(patron_SRT_times, read_lyric_file(file_URL))

def create_SRT_obj(file_URL:str):
  dict = {
    "subtitles": get_SRT_subs(file_URL),
    "times": []
  }

  for time in get_SRT_times(file_URL):
      start, end = time
      # parse text to seconds
      start = timedelta(hours=int(start[:2]), minutes=int(start[3:5]), seconds=int(start[6:8]), milliseconds=int(start[9:])).total_seconds()
      end = timedelta(hours=int(end[:2]), minutes=int(end[3:5]), seconds=int(end[6:8]), milliseconds=int(end[9:])).total_seconds()

      
      dict["times"].append({"start":start, "end": end})
  return SRT_Object(dict)
      
class SRT_Object:
  def __init__(self, data:dict) -> None:
    self.subtitles = data["subtitles"]
    self.times = data["times"]


def get_LRC_lyrics(file_URL:str):
    lines = read_lyric_file(file_URL).split('\n')
    lyrics = []
    for line in lines:
        if line.startswith('['):
            lrc_matches = re.search(r'\[(\d+):(\d+)\]', line)
            if lrc_matches == None: 
                lrc_matches = re.search(r'\[(\d+):(\d+).(\d+)\]', line)

            time_str, lyric = line.split(']')

            if lyric.startswith(' '):
                lyric = lyric[1:]

            mins = int(lrc_matches.group(1))
            secs = int(lrc_matches.group(2))

            seconds = (mins * 60) + secs

            #seconds = timedelta(minutes=int(time_str[1:3]), seconds=int(time_str[4:6]), milliseconds=int(time_str[7:9])).total_seconds()
            #CREATE LIST OF DICTS WITH KEYS "times" and "lyric" 
            lyrics.append({"time": seconds, "lyric": lyric})
    return lyrics

def create_LRC_object(file_URL:str):
  dict = {
    "lyrics": get_LRC_lyrics(file_URL),
  }
  return LRC_Object(dict)

class LRC_Object:
  def __init__(self, data:dict) -> None:
    self.lyricsList = data["lyrics"]


class LyricObject:
  def __init__(self, lyric_file:str) -> None:
    if lyric_file == None: return None
    if lyric_file.endswith(".lrc"):
      self.format = "LRC"
      self.lyricsList = create_LRC_object(lyric_file).lyricsList
    elif lyric_file.endswith(".srt"):
      self.format = "SRT"
      srt = create_SRT_obj(lyric_file)
      self.subtitles = srt.subtitles
      self.times = srt.times
    else: return None
  
