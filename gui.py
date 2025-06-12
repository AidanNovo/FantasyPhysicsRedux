import tkinter as tk
from tkinter import ttk
import math

import common
import gui_theme

# This module exists for organizational reasons, to split all the tkinter code (or most of it) off into its own place.

# TODO: Consider further organizing the GUI code by implementing functions that create distinct GUI elements.
#  e.g. create_sidebar() that initializes all the sidebar code.
#  That said, I am not sure this will help. May just add in a layer of bloat.


def update_deck_display():
    for card in common.deck.list:
        deck_index = common.deck.list.index(card)
        card.gui_button.grid(row=math.floor(deck_index / 3), column=deck_index % 3, padx=2, pady=2)

    root.after(100, update_deck_display)


def update_active_row_display(repeat=True):
    # Show the max # of tokens you can have
    active_row_label.configure(text=f'ACTIVE ROW ({len(common.active_row.list)}/{common.active_row.max_length})')

    for card in common.active_row.list:
        card.gui_button.grid(row=1, column=common.active_row.list.index(card))

        # Update token string
        if card.power_slots != 0:
            card.token_string = '(P)'*card.power_tokens + '( )'*(card.power_slots - card.power_tokens)

        # Update card status string to reflect any changes.
        card.gui_button.configure(text=card.status_string())

    if repeat:
        root.after(100, update_active_row_display)


def update_particle_row_display(repeat=True):
    for token in common.particle_row.list:
        token.gui_button.grid(row=1, column=common.particle_row.list.index(token))

    if repeat:
        root.after(100, update_particle_row_display)


def update_power_row_display(repeat=True):
    # Show the max # of tokens you can have
    power_row_label.configure(text=f'POWER TOKENS ({len(common.power_row.list)}/{common.power_row.max_length})')

    for token in common.power_row.list:
        token.gui_button.grid(row=1, column=common.power_row.list.index(token))


    if repeat:
        root.after(100, update_power_row_display)


def update_stat_display():
    stat_display_label.config(text=f'SCORE: {common.score}  |  DATA:  {common.data}')
    root.after(100, update_stat_display)


if __name__ == '__main__':
    # UI STUFF BELOW HERE
    root = tk.Tk()
    gui_theme.set_style(root)
    root.title('FantasyPhysics')

    # Sidebar stuff
    F_sidebar = ttk.Frame(root)
    F_sidebar.grid(row=0, column=0, rowspan=4, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.N + tk.S)

    # Stat display
    stat_display_label = ttk.Label(F_sidebar, text='SCORE: 0')
    stat_display_label.grid(row=3, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E)

    # Deck list
    decklist_label = ttk.Label(F_sidebar, text='DECK LIST', font='Helvetica 18 bold')
    decklist_label.grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E)

    F_deck_images = ttk.Frame(F_sidebar)
    F_deck_images.grid(row=2, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N + tk.S)

    C_deck_canvas = tk.Canvas(F_deck_images, width=340, height=580, scrollregion=(0, 0, 0, 800), yscrollincrement=15)
    deck_vbar = ttk.Scrollbar(F_deck_images, orient=tk.VERTICAL, command=C_deck_canvas.yview)
    C_deck_canvas.configure(yscrollcommand=deck_vbar.set)

    F_internal_deck_frame = ttk.Frame(C_deck_canvas)
    F_internal_deck_frame.bind("<Configure>", lambda e: C_deck_canvas.configure(scrollregion=C_deck_canvas.bbox("all")))

    C_deck_canvas.create_window((0, 0), window=F_internal_deck_frame, anchor="nw")
    C_deck_canvas.pack(side=tk.LEFT)
    deck_vbar.pack(side=tk.RIGHT, fill=tk.Y)

    common.deck.gui_frame = F_internal_deck_frame

    def _on_mousewheel(event):
        direction = 0
        if event.num == 5 or event.delta < 0:
            direction = 1
        elif event.num == 4 or event.delta > 0:
            direction = -1

        C_deck_canvas.yview_scroll(direction, "units")

    C_deck_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Active row
    F_active_row = ttk.Frame(root, height=140)
    F_active_row.grid(row=0, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)
    active_row_label = ttk.Label(F_active_row, text='ACTIVE ROW')
    active_row_label.grid(row=0, column=0, columnspan=common.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                          sticky=tk.W + tk.S + tk.E)
    common.active_row.gui_frame = F_active_row

    # Particle token row
    F_particle_row = ttk.Frame(root, height=140)
    F_particle_row.grid(row=1, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)
    particle_row_label = ttk.Label(F_particle_row, text='PARTICLE TOKENS')
    particle_row_label.grid(row=0, column=0, columnspan=common.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                          sticky=tk.W + tk.S + tk.E)
    common.particle_row.gui_frame = F_particle_row

    # Power token row
    F_power_row = ttk.Frame(root, height=140)
    F_power_row.grid(row=2, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)
    power_row_label = ttk.Label(F_power_row, text='POWER TOKENS')
    power_row_label.grid(row=0, column=0, columnspan=common.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                         sticky=tk.W + tk.S + tk.E)
    common.power_row.gui_frame = F_power_row

    # Controls
    F_controls = ttk.Frame(root)
    F_controls.grid(row=3, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.E + tk.W + tk.S)
    controls_label = ttk.Label(F_controls, text='CONTROLS')
    controls_label.grid(row=0, column=0, columnspan=common.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                        sticky=tk.W + tk.S + tk.E)

    from main import crack_booster_pack
    booster_button = ttk.Button(F_controls, text='Open Booster', command=crack_booster_pack, takefocus=False)
    booster_button.grid(row=1, column=0)

    from main import activate_cards
    activate_cards_button = ttk.Button(F_controls, text='Activate Cards', command=lambda: activate_cards(root), takefocus=False)
    activate_cards_button.grid(row=1, column=1)

    from main import get_all_cards
    card_sampler_button = ttk.Button(F_controls, text='Get 1 of Each Card', command=get_all_cards, takefocus=False)
    card_sampler_button.grid(row=1, column=2)

    common.do_slow_activation = tk.IntVar()
    slow_activate_checkbox = ttk.Checkbutton(F_controls, variable=common.do_slow_activation, takefocus=False,
                                            text= 'Press space to advance activation   ')
    slow_activate_checkbox.grid(row=1, column=3)

    root.after(0, update_stat_display)
    root.after(0, update_deck_display)
    root.after(0, update_active_row_display)
    root.after(0, update_particle_row_display)
    root.after(0, update_power_row_display)

    # create_item('Power', common.deck)
    # create_item('e- Neutrino', common.particle_row)
    # create_item('Muon Neutrino', common.particle_row)
    # create_item('Tau Neutrino', common.particle_row)

    root.mainloop()