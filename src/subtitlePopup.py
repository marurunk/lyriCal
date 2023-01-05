from tkinter.font import Font
import src.timeliner as timeliner
import src.music as music
from tkinter import *
from ctypes import windll


MIN_WIDTH = 200
MIN_HEIGHT = 60

BG_OPACITY = 0.5

TRANSPARENT_COLOR = "#111"

BG_COLOR = "#000"

class SubtitleWindow(Tk):
    def __init__(self):
        super().__init__()
        
        ROBOTO_FONT = Font(family="data/Roboto-Bold.ttf", size=20)


        self.overrideredirect(True)
        self.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.wm_attributes("-toolwindow", True)
        self.wm_attributes("-topmost", True)
        self.config(bg=TRANSPARENT_COLOR)

        self.label_subtitle = Label(self, text="", bg=TRANSPARENT_COLOR, fg="white", bd=0, padx=20, pady=6)
        self.label_subtitle.pack(fill=BOTH, expand=TRUE)
        self.label_subtitle.config(font=ROBOTO_FONT)
        
        self.background_window = Toplevel()
        self.background_window.overrideredirect(True)
        self.background_window.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.background_window.config(bg=BG_COLOR)
        self.background_window.wm_attributes("-alpha", BG_OPACITY)
        self.background_window.wm_attributes("-topmost", True)
        
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Motion>", self.on_motion)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<Activate>", self.on_focus_in)
        self.bind("<k>", self.pause)
        
        self.background_window.bind("<ButtonPress-1>", self.on_press)
        self.background_window.bind("<ButtonRelease-1>", self.on_release)
        self.background_window.bind("<Motion>", self.on_motion)
        
        self.background_window.protocol("WM_DELETE_WINDOW", self.destroy_both)
        
        self.update()
        self.lift()
        # self.after(10, set_appwindow, self)
        
        #LOGIC
        self.old_x, self.old_y = None, None
        

    def destroy_both(self):
        self.background_window.after(0, self.background_window.destroy)
        self.destroy()
    
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
            self.geometry("+{}+{}".format(self.winfo_x() + deltax, self.winfo_y() + deltay))
            self.background_window.geometry("+{}+{}".format(self.winfo_x() + deltax, self.winfo_y() + deltay))
            
            self.old_center_x = self.winfo_x() + (self.winfo_width()/2)
            self.old_center_y = self.winfo_y() + (self.winfo_height()/2)
            
            self.lift()
            self.focus_force()
            

    def on_focus_in(self, event):
        self.background_window.lift()
        self.lift()
        
    def move_center(self):
        # Obtenga el ancho y alto de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Obtenga el ancho y alto de la ventana
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Calcule la posición x e y para centrar la ventana
        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)

        # Mueva la ventana al centro de la pantalla
        self.geometry(f"+{x_pos}+{y_pos}")
        self.background_window.geometry(f"+{x_pos}+{y_pos}")
    
    def fix_position(self):
        
        self.geometry(f"+{int(self.old_center_x-(self.winfo_width())/2)}+{int(self.old_center_y-(self.winfo_height()/2))}")
        self.background_window.geometry(f"+{int(self.old_center_x-(self.winfo_width()/2))}+{int(self.old_center_y-(self.winfo_height()/2))}")
        


    def set_txt(self, txt):
        self.label_subtitle.config(text=txt)
        if self.label_subtitle["text"] != "":
            self.update_geometry()       
        
    def pause(self, event):
        #if music.Player.playing:
        #    music.Player.pause()
        #else:
        #    music.Player.play()
        music.reproductor.pause()

    def update_geometry(self):
        self.old_center_x = self.winfo_x() + (self.winfo_width()/2)
        self.old_center_y = self.winfo_y() + (self.winfo_height()/2)

        self.geometry(f"{self.label_subtitle.winfo_reqwidth()}x{self.label_subtitle.winfo_reqheight()}")
        self.background_window.geometry(f"{self.label_subtitle.winfo_reqwidth()}x{self.label_subtitle.winfo_reqheight()}")

        self.fix_position()
