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
        create_item(c, holder=vars.deck)

    print('Deck:', vars.deck.list)


def get_all_cards():
    """Add one copy of each card in card_dict to the deck."""
    for card_name in cards.card_dict.keys():
        create_item(card_name, holder=vars.deck)


def show_big_card(event, card):
    """Create a window displaying a larger version of a card."""
    popup = tk.Toplevel(root)
    big_image = card.large_image
    image_label = tk.Label(popup, image=big_image)
    image_label.pack()


def create_item(item_name, holder):
    if len(holder.list) == holder.max_length:
        print(f'Could not add item to {holder}.')

    else:
        item = cards.card_factory(item_name)

        base_img = Image.open(item.image_file)
        item.image = ImageTk.PhotoImage(base_img.resize((100, 140)))
        item.large_image = ImageTk.PhotoImage(base_img.resize((250, 350)))

        item.gui_button = tk.Button(holder.gui_frame, image=item.image)

        holder.list.append(item)

        holder.list[-1].function = holder.list[-1].function.__get__(holder.list[-1], type(item))  # Bind instance method

        item.gui_button.bind('<Button-2>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-2 on Mac
        item.gui_button.bind('<Button-3>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-3 on PC

        if holder == vars.deck:  # Deck specific for now
            item.gui_button.configure(command=lambda c=item: move_item(c, vars.deck, vars.active_row))
            item_index = holder.list.index(item)
            item.gui_button.grid(row=math.floor(item_index / 3), column=item_index % 3, padx=2, pady=2)


def move_item(item, old_holder, new_holder):
    if len(new_holder.list) == new_holder.max_length:
        print(f'Could not add item to {new_holder}.')
    else:
        cfg = item.gui_button.config()
        item.gui_button.destroy()

        old_index = old_holder.list.index(item)
        new_holder.list.append(old_holder.list.pop(old_index))

        item.gui_button = tk.Button(new_holder.gui_frame, image=cfg['image'][4], compound=tk.TOP)

        if new_holder == vars.active_row:
            item.gui_button.configure(command=lambda c=item: move_item(c, vars.active_row, vars.deck),
                                      compound=tk.TOP)
            item.gui_button.grid(row=0, column=vars.active_row.list.index(item))

        elif new_holder == vars.deck:
            item.gui_button.configure(command=lambda c=item: move_item(c, vars.deck, vars.active_row),
                                      compound=tk.NONE)
            item_index = new_holder.list.index(item)
            item.gui_button.grid(row=math.floor(item_index / 3), column=item_index % 3, padx=2, pady=2)

        item.gui_button.bind('<Button-2>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-2 on Mac
        item.gui_button.bind('<Button-3>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-3 on PC

# TODO: For convenience, add a button to reset the current active row.
# def reset():
#     vars.active_row = []
#     vars.deck = []

def activate_cards():
    print('\nCard order:', vars.active_row.list)

    print('\n--------START--------')
    print('Allocating grid power tokens...')
    cards.allocate_power_tokens(-1, vars.active_row.list)

    for card in vars.active_row.list:
        card.function(vars.active_row.list, root)

    print('---------END---------')


def update_deck_display():
    for card in vars.deck.list:
        deck_index = vars.deck.list.index(card)
        card.gui_button.grid(row=math.floor(deck_index / 3), column=deck_index % 3, padx=2, pady=2)

    root.after(250, update_deck_display)


def update_active_row_display(repeat=True):
    for card in vars.active_row.list:
        card.gui_button.grid(row=0, column=vars.active_row.list.index(card))

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
    vars.active_row.gui_frame = F_active_cards

    F_deck_images = ttk.Frame(F_sidebar)
    F_deck_images.grid(row=2, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N + tk.S)

    C_deck_canvas = tk.Canvas(F_deck_images, width=340, height=500, scrollregion=(0, 0, 0, 800), yscrollincrement=15)
    deck_vbar = ttk.Scrollbar(F_deck_images, orient=tk.VERTICAL, command=C_deck_canvas.yview)
    C_deck_canvas.configure(yscrollcommand=deck_vbar.set)

    F_internal_deck_frame = ttk.Frame(C_deck_canvas)
    F_internal_deck_frame.bind("<Configure>", lambda e: C_deck_canvas.configure(scrollregion=C_deck_canvas.bbox("all")))

    vars.deck.gui_frame = F_internal_deck_frame


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
