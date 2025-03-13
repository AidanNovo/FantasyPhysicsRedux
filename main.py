import random
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import math

import cards
import vars
import time
from copy import deepcopy


# TODO: Implement a GUI to reorganize your active row

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

    # TODO: Implement random booster pack contents

    pulled_cards = random.choices(population=draw_pool, weights=draw_weights, k=pack_size)

    for c in pulled_cards:
        print(f'You found a(n) {c} card!')
        add_card_to_deck(c)

    print('Deck:', vars.deck)


j = 0

def add_card_to_deck(card_name):
    """Add a card by name to the deck, bind its function to the instance, and grid the corresponding button."""

    card = cards.card_factory(card_name)
    card.image = tk.PhotoImage(file=card.image_file)  # Would be more memory-efficient to point to a shared PhotoImage
    card.gui_button = tk.Button(F_deck_images, image=card.image)

    vars.deck.append(card)  # Add new card object
    vars.deck[-1].function = vars.deck[-1].function.__get__(vars.deck[-1], cards.Card)  # Bind instance method

    card.gui_button.configure(command=lambda c=card: move_card_to_active_row(c))
    # Grid the corresponding GUI button into the deck frame
    deck_index = vars.deck.index(card)
    card.gui_button.grid(row=math.floor(deck_index/3), column=deck_index % 3, padx=2, pady=2)



def move_card_to_active_row(card):
    deck_index = vars.deck.index(card)

    if len(active_row) < vars.max_active_cards:
        print(f'Moving card from deck index {deck_index} to active row')
        cfg = card.gui_button.config()
        card.gui_button.destroy()
        active_row.append(vars.deck.pop(deck_index))
        card.gui_button = tk.Button(F_active_cards, image=cfg['image'][4], command=cfg['command'][4])
        card.gui_button.grid(row=0, column=active_row.index(card))
    else:
        print(f'Free up a slot in the active row first!')

# TODO: For convenience, add a button to reset the current active row.
# def reset():
#     active_row = []
#     vars.deck = []

def activate_cards():
    print('\nCard order:', active_row)

    print('\n--------START--------')
    for card in active_row:
        active_card_pointer.grid(row=1, column=active_row.index(card))
        root.update()
        root.update_idletasks()
        card.function(active_row)
        time.sleep(1)

    active_card_pointer.grid_remove()
    print('---------END---------')


def update_deck_display():
    # for card in vars.deck:
    #     card.gui_button.grid_forget()

    for card in vars.deck:
        deck_index = vars.deck.index(card)
        card.gui_button.grid(row=math.floor(deck_index / 3), column=deck_index % 3, padx=2, pady=2)

    root.after(250, update_deck_display)

    # def update_deck_display():
#     try:
#         for card in card_button_list:
#             card.configure(image=image_dict[vars.deck[card_button_list.index(card)].image_file])
#     except IndexError:
#         card.configure(image=placeholder_img)  # This may be wasting some resources? But it is quick and easy.
#         # print('IndexError')
#     root.after(250, update_deck_display)


# def update_active_row_display():
#     try:
#         for item in active_item_label_list:
#             item.config(image=image_dict[active_row[active_item_label_list.index(item)].image_file])
#     except IndexError:
#         pass

    # root.after(250, update_active_row_display)


def update_score():
    score_label.config(text=f'SCORE: {vars.score}')
    root.after(250, update_score)

if __name__ == '__main__':
    # print('-----------------------------------------------------------------------------\n'
    #       'Welcome to the prototype for the redesigned fantasy physics outreach project!\n'
    #       '\n'
    #       'Commands:\n'
    #       'o - open a booster pack\n'
    #       'l - list available cards\n'
    #       'a - add cards of your choice to your deck\n'
    #       'd - view your deck\n'
    #       'h - display this message again\n'
    #       '-----------------------------------------------------------------------------\n')

    # UI STUFF BELOW HERE
    root = tk.Tk()
    placeholder_img = PhotoImage(file='fp_small_placeholder.png')
    # ic_img = PhotoImage(file='fp_small_icecube.png')
    # neutrino_img = PhotoImage(file='fp_small_neutrino_gen.png')
    # retrigger_img = PhotoImage(file='fp_small_retrigger.png')
    # ml_img = PhotoImage(file='fp_small_ml.png')
    # recompute_img = PhotoImage(file='fp_small_recompute.png')

    # image_dict = {
    #     'fp_small_placeholder.png': placeholder_img,
    #     'fp_small_icecube.png': ic_img,
    #     'fp_small_neutrino_gen.png': neutrino_img,
    #     'fp_small_retrigger.png': retrigger_img,
    #     'fp_small_ml.png': ml_img,
    #     'fp_small_recompute.png': recompute_img
    # }

    active_row = []

    F_sidebar = tk.Frame(root, bd=2, bg='#bbbbbb', relief=tk.GROOVE)
    F_sidebar.grid(row=0, column=0, rowspan=2, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.N + tk.S)

    decklist_label = tk.Label(F_sidebar, text='DECK LIST', bg='#777777', padx=125, pady=20)
    decklist_label.grid(row=1, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E)

    F_active_cards = tk.Frame(root)
    F_active_cards.grid(row=0, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)

    active_card_pointer = tk.Label(F_active_cards, text='ACTIVE')

    F_deck_images = tk.Frame(F_sidebar, width=350, height=450)
    F_deck_images.grid(row=2, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N + tk.S)

    score_label = tk.Label(F_sidebar, text='SCORE: 0', bg='#777777', padx=125, pady=20)
    score_label.grid(row=3, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E)

    F_controls = tk.Frame(root, bd=2, bg='#bbbbbb', relief=tk.GROOVE)
    F_controls.grid(row=1, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.E + tk.W)
    controls_label = tk.Label(F_controls, text='CONTROLS', bg='#777777', padx=250, pady=20)
    controls_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.S + tk.E)

    booster_button = tk.Button(F_controls, text='Open Booster', command=crack_booster_pack)
    booster_button.grid(row=1, column=0)

    activate_cards_button = tk.Button(F_controls, text='Activate Cards', command=activate_cards)
    activate_cards_button.grid(row=1, column=1)

    # reset_button = tk.Button(F_controls, text='Reset', command=reset)
    # reset_button.grid(row=1, column=2)

    root.after(0, update_score)
    root.after(0, update_deck_display)
    # root.after(0, update_active_row_display)

    root.mainloop()

    # crack_booster_pack()
    #
    # # This is the 'on-screen' row that contains the currently active card_dict.
    # active_row = [vars.deck[-1], vars.deck[1], vars.deck[2], vars.deck[3]]
    # print('Card order:', active_row)
    #
    # print('\n--------START--------')
    # for item in active_row:
    #     item.function(active_row)
    #
    # print('---------END---------')
    # print(f'Score: {vars.score}')
