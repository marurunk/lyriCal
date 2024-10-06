import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from colors import *


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hello World")

        self.b_vol = Gtk.VolumeButton()
        self.b_vol.connect("value-changed", self.on_vol_clicked)
        self.add(self.b_vol)

    def on_button_clicked(self, widget):
        print("Hello World")
    def on_vol_clicked(self):
        cRED()
        print("on_vol_clicked: ")
        cWHITE()



win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
