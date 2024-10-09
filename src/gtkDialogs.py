import os
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# ------ get user dirs ----------
user_home = ""
user_desktop = ""
user_music = ""
user_docs = ""
user_pics = ""
user_videos = ""
user_downloads = "" 
if os.name == 'nt':
    import winreg
    sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
        user_desktop = winreg.QueryValueEx(key, "B4BFCC3A-DB2C-424C-B029-7FE99A87C641")[0]
        user_music = winreg.QueryValueEx(key, "4BD8D571-6D19-48D3-BE97-422220080E43")[0]
        user_docs = winreg.QueryValueEx(key, "FDD39AD0-238F-46AF-ADB4-6C85480369C7")[0]
        user_pics = winreg.QueryValueEx(key,  "33E28130-4E1E-4676-835A-98395C3BC3BB")[0]
        user_videos = winreg.QueryValueEx(key, "18989B1D-99B5-455B-841C-AB7C74E4DDFC")[0]
        user_downloads = winreg.QueryValueEx(key, "374DE290-123F-4565-9164-39C4925E467B")[0]
 
else:
    try:
        user_desktop = subprocess.run(["xdg-user-dir", "DESKTOP"],
                                capture_output=True, text=True).stdout.strip("\n")
        user_music = subprocess.run(["xdg-user-dir", "MUSIC"],
                                capture_output=True, text=True).stdout.strip("\n")
        user_pics = subprocess.run(["xdg-user-dir", "PICTURES"],
                                capture_output=True, text=True).stdout.strip("\n")
        user_docs = subprocess.run(["xdg-user-dir", "DOCUMENTS"],
                                capture_output=True, text=True).stdout.strip("\n")
        user_videos =subprocess.run(["xdg-user-dir", "VIDEOS"],
                                capture_output=True, text=True).stdout.strip("\n")
        user_downloads = subprocess.run(["xdg-user-dir", "DOWNLOAD"],
                                capture_output=True, text=True).stdout.strip("\n")

    except FileNotFoundError:  # if the command is missing
        import os.path
        user_desktop = os.path.expanduser("~/Desktop")  # fallback
        user_music = os.path.expanduser("~/Music")  # fallback
        user_pics = os.path.expanduser("~/Pictures")  # fallback
        user_docs = os.path.expanduser("~/Documents")  # fallback
        user_videos = os.path.expanduser("~/Videos")  # fallback
        user_downloads = os.path.expanduser("~/Downloads")  # fallback
    user_home = os.path.expanduser("~")  # fallback

# --------- || ----------

def selectCarpet() -> str | None:
    dialog = Gtk.FileChooserDialog(
        title="Select a carpet",
        action=Gtk.FileChooserAction.SELECT_FOLDER
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
    dialog.set_current_folder(user_music)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        carpet = dialog.get_filename()
        dialog.destroy()
        return carpet
    else:
        dialog.destroy()
        return None

def selectFile() -> list | None:
    dialog = Gtk.FileChooserDialog(
        title="Seleccionar archivo",
        action=Gtk.FileChooserAction.OPEN
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
    dialog.set_current_folder(user_music)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        archivo = dialog.get_filename()
        print("file selected:", archivo)
        dialog.destroy()
        return [archivo]
    else:
        print("None")
        dialog.destroy()
        return None

def selectMusic():
    dialog = Gtk.FileChooserDialog(
        title="Select files",
        action=Gtk.FileChooserAction.OPEN
    )
    dialog.set_current_folder(user_music)
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    dialog.set_select_multiple(True)

    filter_music = Gtk.FileFilter()
    filter_music.set_name("Music files")
    filter_music.add_mime_type("audio/mp3")
    filter_music.add_mime_type("audio/mpeg")
    filter_music.add_mime_type("audio/wav")
    filter_music.add_mime_type("audio/ogg")
    filter_music.add_mime_type("audio/flac")
    filter_music.add_mime_type("audio/x-m4a")
    filter_music.add_mime_type("audio/x-wavpack")
    filter_music.add_mime_type("audio/x-vorbis+ogg")
    filter_music.add_mime_type("audio/x-opus+ogg")
    filter_music.add_pattern("*.m3u")
    dialog.add_filter(filter_music)

    filter_any = Gtk.FileFilter()
    filter_any.set_name("Any files")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        archivos = dialog.get_filenames()
        for files in archivos:
            print(files)
    else:
        print("None")
    dialog.destroy()

def selectLyric():
    dialog = Gtk.FileChooserDialog(
        title="Select files",
        action=Gtk.FileChooserAction.OPEN
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    dialog.set_select_multiple(False)

    filter_lyric= Gtk.FileFilter()
    filter_lyric.set_name("Lyric files")
    filter_lyric.add_pattern("*.lrc")
    filter_lyric.add_pattern("*.srt")
    dialog.add_filter(filter_lyric)

    filter_any = Gtk.FileFilter()
    filter_any.set_name("Any files")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)


    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        archivos = dialog.get_filenames()
        for files in archivos:
            print(files)
    else:
        print("None")
    dialog.destroy()
