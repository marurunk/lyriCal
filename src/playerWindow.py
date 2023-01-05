from tkinter.font import Font
# import music as music
from tkinter import *
from ctypes import windll
import tkinter.ttk as ttk



GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

def set_appwindow(main_window):
    hwnd = windll.user32.GetParent(main_window.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    main_window.withdraw()
    main_window.after(10, main_window.deiconify)

MIN_WIDTH = 200
MIN_HEIGHT = 300

BG_OPACITY = 0.9

TRANSPARENT_COLOR = "#111"

BG_COLOR = "#fff"

class MusicPlayerWindow(Tk):
    def __init__(self):
        super().__init__()
        
        ROBOTO_FONT = Font(family="data/Roboto-Bold.ttf", size=20)


        self.overrideredirect(False)
        self.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.wm_attributes("-toolwindow", True)
        self.wm_attributes("-topmost", False)
        self.config(bg=TRANSPARENT_COLOR)
        
        self.background_window = Toplevel()
        self.background_window.overrideredirect(False)
        self.background_window.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.background_window.config(bg=BG_COLOR)
        self.background_window.wm_attributes("-alpha", BG_OPACITY)
        self.background_window.wm_attributes("-topmost", False)
        
        self.frame = ttk.Frame(self)

        # self.frame.configure()
        self.frame.pack(expand=True,fill="both", padx=10,pady=10)

        self.old_x, self.old_y = None, None

        ttk.Style().configure("TButton", foreground="blue",font=("data/Roboto-Bold.ttf", 9, "bold"), background=TRANSPARENT_COLOR)
        ttk.Style().configure("TFrame", foreground="blue", background=TRANSPARENT_COLOR)
        ttk.Style().configure("TLabel", foreground="blue", background=TRANSPARENT_COLOR)

        self.label_title = ttk.Label(self.frame, text="MusicPlayer")
        self.label_title.config(font=ROBOTO_FONT)
        
        self.label_title.grid(column=0,row=0,columnspan=3,sticky="nsew")

        self.button_load= ttk.Button(self.frame, text="Load",width=10)
        self.button_load.grid(row=1,column=0)

        self.button_pause = ttk.Button(self.frame, text="Pause",width=10)
        self.button_pause.grid(row=1,column=1)

        self.button_next = ttk.Button(self.frame, text="Next",width=10)
        self.button_next.grid(row=1,column=2)

        self.background_window.bind("<ButtonPress-1>", self.on_press)
        self.background_window.bind("<ButtonRelease-1>", self.on_release)
        self.background_window.bind("<Motion>", self.on_motion)
        self.background_window.protocol("WM_DELETE_WINDOW", self.destroy_both)
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Motion>", self.on_motion)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<Activate>", self.on_focus_in)
        self.bind("<k>", self.pause)
        self.after(10, set_appwindow, self)
        self.move_center()
        self.mainloop()
        
        #LOGIC
        

    def destroy_both(self):
        self.background_window.destroy()
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
        self.label_title.config(text=txt)
        if self.label_title["text"] != "":
            self.update_geometry()       
        
    def pause(self, event):
        # if music.Player.playing:
        #     music.Player.pause()
        # else:
        #     music.Player.play()
        pass  
        
window = MusicPlayerWindow()
