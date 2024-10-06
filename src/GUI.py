import threading
import time
from tkinter import *
from tkinter.constants import BOTH
from tkinter.font import Font
import customtkinter
from src.controller import Controller
from src.colors import *
from src.subtitlePopup import SubtitlePopup
import os

if os.name == "nt":
    from ctypes import windll

#---------------------------------------------#

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

#---------------------------------------------#

MIN_WIDTH, MIN_HEIGHT = 200, 360
RADIUS = 28
BORDER_SIZE = 3

COLOR_BG = "#111"
COLOR_1 = "#3af"
COLOR_2 = "darkblue"
COLOR_3 = "orange"
COLOR_OUTLINE = "#fff"

TRANSPARENT_COLOR = "grey"


class LyriCal_GUI():
    old_x = None
    old_y = None
    load_thread = None
    def __init__(self) -> None:

        self.app = customtkinter.CTk()
        self.subtitlePopup  = SubtitlePopup()
        self.controller = Controller(self)
        self.animation_active = False



        #-----------------------------APP CONFIGURE-------------------------------------#
        
        self.app.title("LyriCal - Music Player")
        self.app.eval('tk::PlaceWindow . center') # Placing the window in the center of the screen
        self.app.title("LyricCal")
        self.app.geometry(f"{MIN_WIDTH}x{MIN_HEIGHT}")
        self.app.config(background='grey')
        self.app.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.app.protocol("WM_DELETE_WINDOW", self.controller.exit)
        if os.name == "nt":
            self.app.attributes("-transparentcolor", TRANSPARENT_COLOR)
            set_appwindow(self.app)


        #self.app.overrideredirect(True) 
                
        #-----------------------------FRONTENT GUI---------------------------------#
        
        self.init_widgets()
        self.configure_widgets()
        
        self.subtitlePopup.unshow()
        #-------------------------ROUNDED BORDERS-----------------------------------#
        
        self.round_rectangle(0, 0, self.app.winfo_width(), self.app.winfo_height(), radius=RADIUS) # Creating the rounded rectangle/window
        self.app.bind("<Configure>", self.draw_round_rectangle)
                
        #------------------------------SHORCUTS----------------------------------#
        
        #minus
        self.app.bind("<k>", self.controller.pause)
        self.app.bind("<j>", self.controller.back_song)
        self.app.bind("<l>", self.controller.next_song)
        
        #mayus
        self.app.bind("<K>", self.controller.pause)
        self.app.bind("<J>", self.controller.back_song)
        self.app.bind("<L>", self.controller.next_song)
        
        self.label_program_title.bind("<ButtonPress-1>", self.on_press)
        self.label_program_title.bind("<ButtonRelease-1>", self.on_release)
        self.label_program_title.bind("<B1-Motion>", self.on_motion)
        #------------------------------------------------------------------------------#
        
        self.app.lift()
        self.app.mainloop()

    def init_widgets(self):
        
        #----------------------------------FONTS-------------------------------------#
        
        PROGRAM_TITLE_FONT = customtkinter.CTkFont(family="Segoe UI Variable", size=20)
        TITLE_FONT = customtkinter.CTkFont(family="data/Roboto-Bold.ttf", size=12)
        ARTIST_FONT = customtkinter.CTkFont(family="data/Roboto-Bold.ttf", size=10)
        BUTTON_FONT = customtkinter.CTkFont(family="data/Roboto-Bold.ttf", size=10)
        SUBTITLE_FONT = Font(family="data/Roboto-Bold.ttf", size=20)
        SONG_FONT = customtkinter.CTkFont(family="data/Roboto-Bold.ttf", size=12)
        
        #------------------------------------------------------------------------------#

        self.subtitlePopup.label_subtitle.config(font=SUBTITLE_FONT)
        
        self.canvas = customtkinter.CTkCanvas(self.app, bg="grey", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)
        
        self.frame = customtkinter.CTkFrame(self.canvas, fg_color=COLOR_BG, bg_color=COLOR_BG)
        self.frame.pack(padx=10,pady=10,fill=BOTH, expand=1)
        
        self.label_program_title = customtkinter.CTkLabel(self.frame, text="LyriCal", font=PROGRAM_TITLE_FONT,
                                               fg_color=(COLOR_BG,"#fff"))
        
        self.box_playlist = Listbox(self.frame,font=SONG_FONT,highlightcolor=COLOR_1,selectbackground=COLOR_1,highlightthickness=0.5)
        
        
        self.bt_load = customtkinter.CTkButton(self.frame, text="Track", font=BUTTON_FONT,
                                                fg_color=(COLOR_1,'white'),hover_color=COLOR_2,bg_color=COLOR_BG,
                                                border_color="black",border_width=2)
        
        self.bt_loadLyric = customtkinter.CTkButton(self.frame, text="Lyric", font=BUTTON_FONT,
                                                fg_color=(COLOR_3, 'white'),hover_color=COLOR_3,bg_color=COLOR_BG,
                                                border_color="black",border_width=2)
        
        self.bt_pause = customtkinter.CTkButton(self.frame, text="Pause", font=BUTTON_FONT,
                                                fg_color=(COLOR_1, 'white'),hover_color=COLOR_2,bg_color=COLOR_BG,
                                                border_color="black",border_width=2)
                                               
        self.bt_back = customtkinter.CTkButton(self.frame, text="Back", font=BUTTON_FONT,
                                                fg_color=(COLOR_1,'white'),hover_color=COLOR_2,bg_color=COLOR_BG,
                                                border_color="black",border_width=2)
                                               
        self.bt_next = customtkinter.CTkButton(self.frame, text="Next", font=BUTTON_FONT,
                                                fg_color=(COLOR_1,'white'),hover_color=COLOR_2,bg_color=COLOR_BG,
                                                border_color="black",border_width=2)

        
        self.label_song_title = customtkinter.CTkLabel(self.frame, text="", font=TITLE_FONT,
                                               fg_color=(COLOR_BG,"white"), anchor="center")
        
        self.label_song_artist = customtkinter.CTkLabel(self.frame, text="", font=ARTIST_FONT,
                                               fg_color=(COLOR_BG,"#eee"), anchor="center")


        self.bt_shuffle= customtkinter.CTkButton(self.frame, text="Shuffle", font=BUTTON_FONT,
                                                fg_color=(COLOR_BG, '#aaf'),hover_color=COLOR_2,bg_color=COLOR_BG,
                                                border_color="black",border_width=2)

        #------------------------------------------------------------------------------#
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=3)
        self.frame.grid_rowconfigure(2, weight=3)
        self.frame.grid_rowconfigure(3, weight=0)
        self.frame.grid_rowconfigure(4, weight=0)
        self.frame.grid_rowconfigure(5, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        
        #------------------------------------------------------------------------------#
        
        self.label_program_title.grid(pady=0,padx=10,
                                                            row=0,column=0,sticky="nsew", columnspan=2)
        self.bt_load.grid(     ipady=2,ipadx=1,pady=10,padx=2,
                                                            row=0,column=2,sticky="nsew")
        self.bt_loadLyric.grid(ipady=2,ipadx=1,pady=10,padx=2,
                                                            row=0,column=3,sticky="nsew")
        self.box_playlist.grid(pady=10,padx=10,
                                                            row=1,column=0,sticky="nsew", columnspan=4,rowspan=2,)
        
        self.label_song_title.grid(pady=0,padx=10,
                                                            row=3,column=0,sticky="ew",   columnspan=4)
        self.label_song_artist.grid(pady=0,padx=10,
                                                            row=4,column=0,sticky="ew",   columnspan=4)
        
        
        self.bt_back.grid(     ipady=4,ipadx=4,pady=10,padx=2,
                                                            row=5,column=0,sticky="nsew")
        self.bt_pause.grid(    ipady=4,ipadx=4,pady=10,padx=0,
                                                            row=5,column=1,sticky="nsew")
        self.bt_next.grid(     ipady=4,ipadx=4,pady=10,padx=2,
                                                            row=5,column=2,sticky="nsew")
        self.bt_shuffle.grid(     ipady=4,ipadx=4,pady=10,padx=2,
                                                            row=5,column=3,sticky="nsew")

    def configure_widgets(self):
        
        self.bt_load.configure(command=self.load_new_song)
        self.bt_loadLyric.configure(command=self.controller.load_lyric)
        
        self.box_playlist.bind("<Double-Button-1>", self.set_song)
        #enter button ID unfinded
        #self.box_playlist.bind("<Intro>", self.set_song)
        self.box_playlist.bind("<space>", self.controller.pause)
        
        self.bt_pause.configure(command=self.controller.pause)
        self.bt_back.configure(command=self.back_song)
        self.bt_next.configure(command=self.next_song)
        self.bt_shuffle.configure(command=self.shuffle)

        # TITLE ANIMATION LABEL THREAD
        self.animation_active = True
        animation_thread = threading.Thread(target=self.title_animation)
        animation_thread.start()
        # Song selected LABEL THREAD
        song_animation_thread = threading.Thread(target=self.song_animation)
        song_animation_thread.start()
        
        # END MUSIC TIMER THREAD
        next_track_thread = threading.Thread(target=self.next_track_timer)
        next_track_thread.start()

    def next_track_timer(self):
        while self.animation_active:
            time_left =self.controller.musicPlayer.get_time_left()
            if time_left <= 1.0 and self.controller.musicPlayer.player.playing:
                time.sleep(2)
                self.next_song()
                time.sleep(1)
            time.sleep(0.2)

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
            
 
    def load_new_song(self):
        self.load_thread = threading.Thread(target=self.controller.load_new_song())
        self.load_thread.start()
    
    def update_playlist(self):
        self.box_playlist.delete(0,END)
        for title in self.controller.get_titles_songs():
            self.box_playlist.insert(END, title)
        self.update_select_song()

    def update_select_song(self):
        self.box_playlist.select_clear(0,END)
        self.box_playlist.select_set(self.controller.musicPlayer.current_index)
        self.label_song_title.configure(text=self.controller.playlist[self.controller.musicPlayer.current_index])

    def draw_round_rectangle(self, event):
        self.canvas.delete("all")
        self.round_rectangle(0, 0, self.app.winfo_width(), self.app.winfo_height(), radius=RADIUS) # Creating the rounded rectangle/window
        
    def round_rectangle(self, x1, y1, x2, y2, radius:int, **kwargs):
        x1 +=BORDER_SIZE//2
        x2 -=BORDER_SIZE//2
        y1 +=BORDER_SIZE//2
        y2 -=BORDER_SIZE//2
        points = [x1+radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1]

        return self.canvas.create_polygon(points, **kwargs, 
                                          smooth=True, fill=COLOR_BG, 
                                          outline=COLOR_OUTLINE, 
                                          width=BORDER_SIZE)
        
    def move_center(self):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()

        x_pos = (screen_width // 2) - (window_width // 2)
        y_pos = (screen_height // 2) - (window_height // 2)

        self.app.geometry(f"+{x_pos}+{y_pos}")

    def set_song(self, event) -> None:
        index = self.box_playlist.curselection()[0]
        self.controller.set_song(index)
        self.update_select_song()

    def shuffle(self):
        self.controller.shuffle()
        self.update_playlist()


    def next_song(self):
        self.controller.next_song()
        index = self.controller.musicPlayer.current_index
        self.update_select_song()
        
    def back_song(self):
        self.controller.back_song()
        index = self.controller.musicPlayer.current_index
        self.box_playlist.select_clear(0,END)
        self.update_select_song()

    def title_animation(self):
        while self.animation_active:
            if len(self.label_song_title.cget("text")) > 26:
                title : str  = self.label_song_title.cget("text")
                title = list(title)
                a = title[0]
                title.append(a)
                title.pop(0)
                title = "".join(title)
                self.label_song_title.configure(text=title)
            time.sleep(0.2)

    def song_animation(self):
        while self.animation_active:
            if not self.box_playlist.curselection():
                time.sleep(1)
                continue
            else:
                index = self.box_playlist.curselection()[0]
                title : str  = self.box_playlist.get(index)
                if len(title) > 26:
                    title : list = list(title)
                    a = title[0]
                    title.append(a)
                    title.pop(0)
                    self.box_playlist.delete(index)
                    self.box_playlist.insert(index,"".join(title))
                    self.box_playlist.select_set(index)
            time.sleep(0.2)




