import ttkthemes
from tkinter import ttk
import common as c

# Module exists for organizational reasons.
# Serves only to house a function that takes the gui root and sets the style.

# TODO: Make it so that we do not inherit the mac dark theme. Makes the UI look ugly.
def set_style(root):
    bg_color = '#ffffff'

    style = ttk.Style()
    # style = ttkthemes.ThemedStyle()
    # style.theme_use('arc')

    # root.configure(background=my_dark_purple)
    # # style.configure('TButton', padding=5, relief='flat', background=bg_color)
    style.configure('TButton', padding=5, background=c.tcolor_dark_purple, bordercolor='#ff0000')
    style.configure('TFrame', background=c.tcolor_dark_purple)
    # style.configure('TScrollbar', background=c.tcolor_dark_purple, foreground=c.tcolor_dark_purple, troughcolor=my_light_grey)
    # style.configure('TCanvas', background=my_dark_purple, foreground=my_dark_purple)
    style.configure('TLabel', background=c.tcolor_dark_purple, foreground=c.tcolor_dark_purple)


    # style.configure()

    # return style
