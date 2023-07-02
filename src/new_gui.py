# from src.controller import Controller
import flet as ft

MIN_WIDTH = 280
MIN_HEIGHT = 480
TITLE_BAR_HEIGHT = 40
COVER_SIZE = 200

COLOR_BG = "#000000"
COLOR_1 = "#0099FF"
COLOR_2 = "#3F4B74"

current_title = ""
current_artist = ""
current_album = ""

# controller = Controller()

class GUI(ft.UserControl):

    def __init__(self, page:ft.Page):
        self.page = page

    def minimize(self, e):
        self.page.window_minimized = True
        self.page.update()

    def build(self, page:ft.Page):
        return ft.Column([
            ft.Row(
                [
                    ft.WindowDragArea(ft.Container(ft.Text("LyriCal",size=20), 
                                                bgcolor=COLOR_BG,
                                                alignment=ft.alignment.center_left,
                                                padding=ft.Padding(left=20,top=0,bottom=4,right=0)
                                                ), 
                                        expand=True,
                                        height=TITLE_BAR_HEIGHT),
                    
                    ft.Container(content=ft.IconButton(
                                    ft.icons.MINIMIZE, 
                                    on_click = self.minimize,
                                    icon_color="white",
                                    icon_size=16,
                                    width=TITLE_BAR_HEIGHT,
                                    height=TITLE_BAR_HEIGHT
                                ),
                                border_radius=0, 
                                bgcolor=COLOR_BG,
                                ),
                    ft.Container(content=ft.IconButton(
                                    ft.icons.CLOSE, 
                                    on_click = lambda _: page.window_close(),
                                    icon_color="white",
                                    icon_size=16,
                                    width=TITLE_BAR_HEIGHT,
                                    height=TITLE_BAR_HEIGHT
                                ),
                                border_radius=0, 
                                bgcolor=COLOR_BG)
                    
                ],alignment=ft.MainAxisAlignment.SPACE_EVENLY,spacing=0
            ),
            ft.Container(expand=True, bgcolor=COLOR_BG,content=ft.Column(
                [
                    ft.Container(bgcolor=COLOR_2,border_radius=6,expand=True),
                    ft.Container(bgcolor=COLOR_2,height=COVER_SIZE, width=COVER_SIZE,border_radius=6),
                    ft.Text(current_title, size=20),
                    ft.Text("MY FIRST STORY", size=14,color=COLOR_2),
                    ft.Row(
                        [
                            ft.IconButton(ft.icons.SKIP_PREVIOUS),
                            ft.IconButton(ft.icons.PAUSE),
                            ft.IconButton(ft.icons.SKIP_NEXT),
                        ],expand=False,alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Slider(value=0.3)
                    
                ], spacing=10,alignment=ft.MainAxisAlignment.END,horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),padding=10,alignment=ft.alignment.center)
        ]
        )

def main(page: ft.Page):

    def minimize(e):
        page.window_minimized = True
        page.update()

#    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.padding = 1
    page.title = "LyriCal"
    page.bgcolor = COLOR_1
    page.window_min_height = MIN_HEIGHT
    page.window_min_width = MIN_WIDTH
    page.vertical_alignment=ft.MainAxisAlignment.START    
    page.spacing = 0
    page.window_resizable = True
    
    
    
    page.add(
        ft.Row(
             [
                ft.WindowDragArea(ft.Container(ft.Text("LyriCal",size=20), 
                                                bgcolor=COLOR_BG,
                                                alignment=ft.alignment.center_left,
                                                padding=ft.Padding(left=20,top=0,bottom=4,right=0)
                                                ), 
                                    expand=True,
                                    height=TITLE_BAR_HEIGHT),
               
                ft.Container(content=ft.IconButton(
                                ft.icons.MINIMIZE, 
                                on_click = minimize,
                                icon_color="white",
                                icon_size=16,
                                width=TITLE_BAR_HEIGHT,
                                height=TITLE_BAR_HEIGHT
                            ),
                            border_radius=0, 
                            bgcolor=COLOR_BG,
                            ),
                ft.Container(content=ft.IconButton(
                                ft.icons.CLOSE, 
                                on_click = lambda _: page.window_close(),
                                icon_color="white",
                                icon_size=16,
                                width=TITLE_BAR_HEIGHT,
                                height=TITLE_BAR_HEIGHT
                            ),
                            border_radius=0, 
                            bgcolor=COLOR_BG)
               
            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY,spacing=0
        ),
        ft.Container(expand=True, bgcolor=COLOR_BG,content=ft.Column(
            [
                ft.Container(bgcolor=COLOR_2,border_radius=6,expand=True),
                ft.Container(bgcolor=COLOR_2,height=COVER_SIZE, width=COVER_SIZE,border_radius=6),
                ft.Text(current_title, size=20),
                ft.Text("MY FIRST STORY", size=14,color=COLOR_2),
                ft.Row(
                    [
                        ft.IconButton(ft.icons.SKIP_PREVIOUS),
                        ft.IconButton(ft.icons.PAUSE),
                        ft.IconButton(ft.icons.SKIP_NEXT),
                    ],expand=False,alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Slider(value=0.3)
               
            ], spacing=10,alignment=ft.MainAxisAlignment.END,horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),padding=10,alignment=ft.alignment.center)
    )
    
    # gui = GUI(page)
    
    # page.add(gui)
    
    page.window_height = MIN_HEIGHT
    page.window_width = MIN_WIDTH
    page.window_visible = True
    page.update()

MainWindow = ft.app(target=main, view=ft.FLET_APP_HIDDEN)
