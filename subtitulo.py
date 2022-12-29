from tkinter.font import Font
import timeliner

from tkinter import *
from ctypes import windll



GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

def set_appwindow(ventana_principal):
    hwnd = windll.user32.GetParent(ventana_principal.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    ventana_principal.withdraw()
    ventana_principal.after(10, ventana_principal.deiconify)

MIN_ANCHO = 200
MIN_ALTO = 60
class LyricPopup(Tk):
    def __init__(self):
        super().__init__()
        # Agregue aquí el código para inicializar la ventana de Tkinter
        self.overrideredirect(True)
        self.geometry(f"{MIN_ANCHO}x{MIN_ALTO}")
        self.wm_attributes("-transparentcolor", "#111")
        self.wm_attributes("-toolwindow", True)
        self.config(bg="#111")


        fuente = Font(family="Roboto-Bold.ttf", size=20)
        self.etiqueta_subtitulo = Label(self, text="", bg="#111", fg="white", bd=0, padx=20, pady=6)
        self.etiqueta_subtitulo.pack(fill=BOTH, expand=TRUE)
        self.etiqueta_subtitulo.config(font=fuente)
        
        
        
        self.ventana_fondo = Toplevel()
        self.ventana_fondo.overrideredirect(True)
        self.ventana_fondo.geometry(f"{MIN_ANCHO}x{MIN_ALTO}")
        self.ventana_fondo.config(bg="black")
        self.ventana_fondo.wm_attributes("-alpha", 0.3)
        
        self.wm_attributes("-topmost", True)
        self.ventana_fondo.wm_attributes("-topmost", True)
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Motion>", self.on_motion)
        self.ventana_fondo.bind("<ButtonPress-1>", self.on_press)
        self.ventana_fondo.bind("<ButtonRelease-1>", self.on_release)
        self.ventana_fondo.bind("<Motion>", self.on_motion)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<Activate>", self.on_focus_in)
        self.update()
        self.lift()
        self.after(10, set_appwindow, self)


        self.ventana_fondo.protocol("WM_DELETE_WINDOW", self.destroy_both)
        
        self.old_x, self.old_y = None, None
        
        
        #LOGICA
        
        timeliner.start(self)  
        

    def destroy_both(self):
        self.ventana_fondo.after(0, self.ventana_fondo.destroy)
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
            self.ventana_fondo.geometry("+{}+{}".format(self.winfo_x() + deltax, self.winfo_y() + deltay))
            self.geometry("+{}+{}".format(self.winfo_x() + deltax, self.winfo_y() + deltay))
            
            self.old_center_x = self.winfo_x() + (self.winfo_width()/2)
            self.old_center_y = self.winfo_y() + (self.winfo_height()/2)
            
            self.lift()

    def on_focus_in(self, event):
        self.ventana_fondo.lift()
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
        self.ventana_fondo.geometry(f"+{x_pos}+{y_pos}")
    
    def fix_position(self):
        
        self.geometry(f"+{int(self.old_center_x-(self.winfo_width())/2)}+{int(self.old_center_y-(self.winfo_height()/2))}")
        self.ventana_fondo.geometry(f"+{int(self.old_center_x-(self.winfo_width()/2))}+{int(self.old_center_y-(self.winfo_height()/2))}")
        


    def set_txt(self, txt):
        self.etiqueta_subtitulo.config(text=txt)
        if self.etiqueta_subtitulo["text"] != "":
            self.update_geometry()       
        

    def update_geometry(self):
        self.old_center_x = self.winfo_x() + (self.winfo_width()/2)
        self.old_center_y = self.winfo_y() + (self.winfo_height()/2)

        self.geometry(f"{self.etiqueta_subtitulo.winfo_reqwidth()}x{self.winfo_reqheight()}")
        self.ventana_fondo.geometry(f"{self.etiqueta_subtitulo.winfo_reqwidth()}x{self.winfo_reqheight()}")

        self.fix_position()