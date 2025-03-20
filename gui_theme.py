import ttkthemes

# Module exists for organizational reasons.
# Serves only to house a function that takes the gui root and sets the style.
# It is sort of stupid that we have to do it this way, but such is tkinter

def set_style(root):
    bg_color = '#25006C'
    style = ttkthemes.ThemedStyle()
    style.theme_use('arc')
    # style.configure('TButton', padding=5, relief='flat', background=bg_color)
    # style.configure('TFrame', borderwidth=5, background=bg_color)
    # # style.configure('TRoot', background='#bbb')
    # style.configure('TLabel', background=bg_color)

    # style.configure()

    print('tada')
    return style
