import random
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math

import cards
import vars
import time
import gui_theme

# TODO: Implement a GUI to reorganize your active row
# TODO: Implement a basic score attack mode (ala Balatro, Nubby, Luck be a Landlord, etc.)
# TODO: Implement outreach scaling

def crack_booster_pack(pack_size=5,
                       draw_pool=tuple(cards.card_dict.keys()),
                       draw_weights=tuple(int(cards.card_dict[c].rarity) for c in cards.card_dict.keys())):
    """
    Add n randomly-chosen cards to the deck, weighted by rarity, with replacement.

    Args:
        pack_size: The number of cards to draw and add to deck.
        draw_pool: A tuple of cards.card_dict keys comprising the pool to pick cards from.
        draw_weights: The weights to draw cards with. Must be same size as draw_pool.
    """

    print('Opening a booster pack...')

    pulled_cards = random.choices(population=draw_pool, weights=draw_weights, k=pack_size)

    for c in pulled_cards:
        print(f'You found a(n) {c} card!')
        add_card_to_deck(c)

    print('Deck:', vars.deck)


def get_all_cards():
    """Add one copy of each card in card_dict to the deck."""
    for card_name in cards.card_dict.keys():
        add_card_to_deck(card_name)


def show_big_card(event, card):
    """Create a large w"""
    popup = tk.Toplevel(root)
    big_image = card.large_image
    image_label = tk.Label(popup, image=big_image)
    image_label.pack()


def add_card_to_deck(card_name):
    """Add a card by name to the deck, bind its function to the instance, and grid the corresponding button."""

    card = cards.card_factory(card_name)

    base_img = Image.open(card.image_file)
    card.image = ImageTk.PhotoImage(base_img.resize((100, 140)))
    card.large_image = ImageTk.PhotoImage(base_img.resize((250, 350)))

    card.gui_button = tk.Button(F_internal_deck_frame, image=card.image)

    vars.deck.append(card)  # Add new card object
    vars.deck[-1].function = vars.deck[-1].function.__get__(vars.deck[-1], cards.Card)  # Bind instance method

    # Initialize the GUI Button and put it in the deck
    card.gui_button.configure(command=lambda c=card: move_card_to_active_row(c))
    card_index = vars.deck.index(card)
    card.gui_button.bind('<Button-2>', lambda event, c=card: show_big_card(event, c))  # Right-click is Button-2 on Mac
    card.gui_button.bind('<Button-3>', lambda event, c=card: show_big_card(event, c))  # Right-click is Button-3 on PC
    card.gui_button.grid(row=math.floor(card_index/3), column=card_index % 3, padx=2, pady=2)


# TODO: Generalize the move to active row and move to deck commands to allow a move from anywhere.
#   - Essentially, stop assuming that cards will only ever be in either the active row or the deck

def move_card_to_active_row(card):
    old_index = vars.deck.index(card)

    if len(vars.active_row) < vars.max_active_cards:
        print(f'Moving card from deck index {old_index} to active row')
        cfg = card.gui_button.config()
        card.gui_button.destroy()
        vars.active_row.append(vars.deck.pop(old_index))
        card.gui_button = tk.Button(F_active_cards, image=cfg['image'][4],
                                    command=lambda c=card: move_card_to_deck(c), compound=tk.TOP)
        card.gui_button.grid(row=0, column=vars.active_row.index(card))
    else:
        print(f'Free up a slot in the active row first!')

    update_active_row_display(repeat=False)

def move_card_to_deck(card):
    old_index = vars.active_row.index(card)

    print(f'Moving card from active row index {old_index} to deck')
    cfg = card.gui_button.config()
    card.gui_button.destroy()
    vars.deck.append(vars.active_row.pop(old_index))
    card.gui_button = tk.Button(F_internal_deck_frame, image=cfg['image'][4],
                                command=lambda c=card: move_card_to_active_row(c))

    card.gui_button.bind('<Button-2>', lambda event, c=card: show_big_card(event, c))  # Right-click is Button-2 on Mac
    card.gui_button.bind('<Button-3>', lambda event, c=card: show_big_card(event, c))  # Right-click is Button-3 on PC

    new_index = vars.deck.index(card)
    card.gui_button.grid(row=math.floor(new_index/3), column=new_index % 3, padx=2, pady=2)

# TODO: For convenience, add a button to reset the current active row.
# def reset():
#     vars.active_row = []
#     vars.deck = []

def activate_cards():
    print('\nCard order:', vars.active_row)

    print('\n--------START--------')
    print('Allocating grid power tokens...')
    cards.allocate_power_tokens(-1, vars.active_row)

    for card in vars.active_row:
        card.function(vars.active_row, root)

    print('---------END---------')


def update_deck_display():
    for card in vars.deck:
        deck_index = vars.deck.index(card)
        card.gui_button.grid(row=math.floor(deck_index / 3), column=deck_index % 3, padx=2, pady=2)

    root.after(250, update_deck_display)


def update_active_row_display(repeat=True):
    for card in vars.active_row:
        card.gui_button.grid(row=0, column=vars.active_row.index(card))

        # Update token string
        if card.power_slots != 0:
            card.token_string = '(P)'*card.power_tokens + '( )'*(card.power_slots - card.power_tokens)

        # Update card status string to reflect any changes.
        card.gui_button.configure(text=card.status_string())

    if repeat:
        root.after(250, update_active_row_display)


def update_stat_display():
    stat_display_label.config(text=f'SCORE: {vars.score}  |  DATA:  {vars.data}  |  '
                                   f'POWER TOKENS: {vars.unused_power_tokens}')
    root.after(250, update_stat_display)


if __name__ == '__main__':
    # UI STUFF BELOW HERE
    root = tk.Tk()
    gui_theme.set_style(root)
    root.title('FantasyPhysics')

    F_sidebar = ttk.Frame(root)
    F_sidebar.grid(row=0, column=0, rowspan=2, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.N + tk.S)

    decklist_label = ttk.Label(F_sidebar, text='DECK LIST', font='Helvetica 18 bold')
    decklist_label.grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E)

    F_active_cards = ttk.Frame(root, height=140)
    F_active_cards.grid(row=0, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)

    F_deck_images = ttk.Frame(F_sidebar)
    F_deck_images.grid(row=2, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N + tk.S)

    C_deck_canvas = tk.Canvas(F_deck_images, width=340, height=500, scrollregion=(0, 0, 0, 800), yscrollincrement=15)
    deck_vbar = ttk.Scrollbar(F_deck_images, orient=tk.VERTICAL, command=C_deck_canvas.yview)
    C_deck_canvas.configure(yscrollcommand=deck_vbar.set)

    F_internal_deck_frame = ttk.Frame(C_deck_canvas)
    F_internal_deck_frame.bind("<Configure>", lambda e: C_deck_canvas.configure(scrollregion=C_deck_canvas.bbox("all")))

    C_deck_canvas.create_window((0, 0), window=F_internal_deck_frame, anchor="nw")
    C_deck_canvas.pack(side=tk.LEFT)
    deck_vbar.pack(side=tk.RIGHT, fill=tk.Y)


    def _on_mousewheel(event):
        direction = 0
        if event.num == 5 or event.delta < 0:
            direction = 1
        elif event.num == 4 or event.delta > 0:
            direction = -1

        C_deck_canvas.yview_scroll(direction, "units")

    C_deck_canvas.bind_all("<MouseWheel>", _on_mousewheel)


    stat_display_label = ttk.Label(F_sidebar, text='SCORE: 0')
    stat_display_label.grid(row=3, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E)

    F_controls = ttk.Frame(root)
    F_controls.grid(row=1, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.E + tk.W + tk.S)
    controls_label = ttk.Label(F_controls, text='CONTROLS')
    controls_label.grid(row=0, column=0, columnspan=vars.max_active_cards, padx=5, pady=5, ipadx=1, ipady=1,
                        sticky=tk.W + tk.S + tk.E)

    booster_button = ttk.Button(F_controls, text='Open Booster', command=crack_booster_pack, takefocus=False)
    booster_button.grid(row=1, column=0)

    activate_cards_button = ttk.Button(F_controls, text='Activate Cards', command=activate_cards, takefocus=False)
    activate_cards_button.grid(row=1, column=1)

    card_sampler_button = ttk.Button(F_controls, text='Get 1 of Each Card', command=get_all_cards, takefocus=False)
    card_sampler_button.grid(row=1, column=2)

    vars.do_slow_activation = tk.IntVar()
    slow_activate_checkbox = ttk.Checkbutton(F_controls, variable=vars.do_slow_activation, takefocus=False,
                                            text= 'Press space to advance activation')
    slow_activate_checkbox.grid(row=1, column=3)

    root.after(0, update_stat_display)
    root.after(0, update_deck_display)
    root.after(0, update_active_row_display)

    root.mainloop()
