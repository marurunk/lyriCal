from tkinter.font import Font
import src.music as music
from tkinter import *
import os

MIN_WIDTH = 200
MIN_HEIGHT = 60

BG_OPACITY = 0.5

TRANSPARENT_COLOR = "#111"

BG_COLOR = "#000"

class SubtitlePopup():
    def __init__(self):
        
        # ROBOTO_FONT = Font(family="data/Roboto-Bold.ttf", size=20)

        self.app = Toplevel()
        self.app.overrideredirect(True)
        self.app.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        if os.name == "nt":
            self.app.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        
        self.app.wm_attributes("-topmost", True)
        self.app.wm_attributes("-alpha", 0)
        self.app.config(bg=TRANSPARENT_COLOR)
        

        self.label_subtitle = Label(self.app, text="", bg=TRANSPARENT_COLOR, fg="white", bd=0, padx=20, pady=6)
        self.label_subtitle.pack(fill=BOTH, expand=TRUE)
        # self.label_subtitle.config(font=ROBOTO_FONT)
        
        self.background_window = Toplevel()
        self.background_window.overrideredirect(True)
        self.background_window.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.background_window.config(bg=BG_COLOR)
        self.background_window.wm_attributes("-alpha", 0)
        self.background_window.wm_attributes("-topmost", True)
        
        
        self.app.bind("<ButtonPress-1>", self.on_press)
        self.app.bind("<ButtonRelease-1>", self.on_release)
        self.app.bind("<Motion>", self.on_motion)
        self.app.bind("<FocusIn>", self.on_focus_in)
        self.app.bind("<Activate>", self.on_focus_in)
        self.app.bind("<k>", self.pause)
        
        self.background_window.bind("<ButtonPress-1>", self.on_press)
        self.background_window.bind("<ButtonRelease-1>", self.on_release)
        self.background_window.bind("<Motion>", self.on_motion)
        
        self.background_window.protocol("WM_DELETE_WINDOW", "WM_DELETE_WINDOW")
        self.app.protocol("WM_DELETE_WINDOW", "WM_DELETE_WINDOW")
        
        
        #LOGIC
        self.old_x, self.old_y = None, None
        self.old_center_x = (self.app.winfo_screenwidth()//2) - (self.app.winfo_width()//2)
        self.old_center_y = (self.app.winfo_screenheight()-100) - (self.app.winfo_height()//2)
        self.app.geometry(f"+{self.old_center_x}+{self.old_center_y}")

    def show(self):
        self.app.wm_attributes("-alpha", 1 )   
        self.background_window.wm_attributes("-alpha", BG_OPACITY)     
    def unshow(self):
        self.app.wm_attributes("-alpha", 0 )   
        self.background_window.wm_attributes("-alpha", 0)     

    def destroy_both(self):
        self.background_window.after(0, self.background_window.destroy)
        self.app.destroy()
    
    def on_press(self, event):
        # obtener la posición del mouse al presionar el botón izquierdo
        self.old_x, self.old_y = event.x, event.y

    def on_release(self, event):
        # resetear la posición del mouse al soltar el botón izquierdo
        self.old_x, self.old_y = None, None
        

    def on_motion(self, event):
        # mover la ventana si se está presionando el botón izquierdo del mouse
        if self.old_x is not None and self.old_y is not None:
            deltax = event.x - self.old_x
            deltay = event.y - self.old_y
            self.app.geometry("+{}+{}".format(self.app.winfo_x() + deltax, self.app.winfo_y() + deltay))
            self.background_window.geometry("+{}+{}".format(self.app.winfo_x() + deltax, self.app.winfo_y() + deltay))
            
            self.old_center_x = self.app.winfo_x() + (self.app.winfo_width()/2)
            self.old_center_y = self.app.winfo_y() + (self.app.winfo_height()/2)
            
            self.app.lift()
            self.app.focus_force()
            

    def on_focus_in(self, event):
        self.background_window.lift()
        self.app.lift()
        
    def move_center(self):
        # Obtenga el ancho y alto de la pantalla
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        # Obtenga el ancho y alto de la ventana
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()

        # Calcule la posición x e y para centrar la ventana
        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)

        # Mueva la ventana al centro de la pantalla
        self.app.geometry(f"+{x_pos}+{y_pos}")
        self.background_window.geometry(f"+{x_pos}+{y_pos}")
        
        self.old_x, self.old_y = None, None
        
        self.old_center_x = (screen_width // 2) - (self.app.winfo_width()//2)
        self.old_center_y = (screen_height // 2) - (self.app.winfo_height()//2)
    
    def fix_position(self):
        
        self.app.geometry(f"+{int(self.old_center_x-(self.app.winfo_width())/2)}+{int(self.old_center_y-(self.app.winfo_height()/2))}")
        self.background_window.geometry(f"+{int(self.old_center_x-(self.app.winfo_width()/2))}+{int(self.old_center_y-(self.app.winfo_height()/2))}")
        


    def set_txt(self, txt):
        self.label_subtitle.config(text=txt)
        if self.label_subtitle["text"] != "":
            self.update_geometry()       
        
    def pause(self, event):
        music.reproductor.pause()

    def destroy(self):
        self.app.destroy()
        self.background_window.destroy()

    def update_geometry(self):

        self.app.geometry(f"{self.label_subtitle.winfo_reqwidth()}x{self.label_subtitle.winfo_reqheight()}")
        self.background_window.geometry(f"{self.label_subtitle.winfo_reqwidth()}x{self.label_subtitle.winfo_reqheight()}")

        self.fix_position()
