
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

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        archivos = dialog.get_filenames()
        for files in archivos:
            print(files)
    else:
        print("None")
    dialog.destroy()

selectFiles()
