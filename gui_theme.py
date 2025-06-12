import ttkthemes

# Module exists for organizational reasons.
# Serves only to house a function that takes the gui root and sets the style.

# TODO: Make it so that we do not inherit the mac dark theme. Makes the UI look ugly.
def set_style(root):
    bg_color = '#ffffff'
    style = ttkthemes.ThemedStyle()
    style.theme_use('arc')
    # root.configure(background=bg_color)
    # # style.configure('TButton', padding=5, relief='flat', background=bg_color)
    # style.configure('TFrame', background=bg_color)
    # style.configure('TCanvas', background=bg_color)
    # # style.configure('TRoot', background='#bbb')
    # style.configure('TLabel', background=bg_color)

    # style.configure()

    return style
