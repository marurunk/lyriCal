
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
        print("Carpet selected:", carpet)
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

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        archivo = dialog.get_filename()
        print("file selected:", archivo)
        dialog.destroy()
        return [archivo]
    else:
        dialog.destroy()
        return None

def selectFiles():
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
    
    dialog.add_filter(filter_music)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        archivos = dialog.get_filenames()
        for files in archivos:
            print(files)
    else:
        print("None")
    dialog.destroy()

selectFiles()
