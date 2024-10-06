import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def selectCarpet() -> str | None:
    dialog = Gtk.FileChooserDialog(
        title="Select a carpet",
        action=Gtk.FileChooserAction.SELECT_FOLDER
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        carpet = dialog.get_filename()
        print(carpet)
        dialog.destroy()
        return carpet
    else:
        dialog.destroy()
        print("None")
        return None

def selectFile() -> list | None:
    dialog = Gtk.FileChooserDialog(
        title="Seleccionar archivo",
        action=Gtk.FileChooserAction.OPEN
    )
    dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

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
