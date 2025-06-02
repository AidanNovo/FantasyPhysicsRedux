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
# TODO: Fix bug where right clicking tokens sometimes crashes the program




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
    #TODO: For some reason this sometimes does not work with tokens.
    global root

    popup = tk.Toplevel(root)
    big_image = card.large_image
    image_label = tk.Label(popup, image=big_image)
    image_label.pack()


def initialize_item_gui_button(item, holder):
    """Initialize the item's gui button and bind the right-click functionality."""
    item.gui_button = tk.Button(holder.gui_frame)
    item.gui_button.bind('<Button-2>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-2 on Mac
    item.gui_button.bind('<Button-3>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-3 on PC


def initialize_item_image(item):
    """Initialize the various images for the item."""
    base_img = Image.open(item.image_file)
    item.image = ImageTk.PhotoImage(base_img.resize((100, 140)))
    item.large_image = ImageTk.PhotoImage(base_img.resize((250, 350)))

    item.gui_button.configure(image=item.image)


def bind_item_instance_function(item, holder, h_index):
    holder.list[h_index].function = holder.list[h_index].function.__get__(holder.list[h_index],
                                                                          type(item))  # Bind instance method


def create_item(item_name, holder, h_index=-1):
    if len(holder.list) == holder.max_length:
        print(f'Could not add item to {holder}.')

    else:
        # Create the item object
        item = cards.item_factory(item_name)

        initialize_item_gui_button(item, holder)

        initialize_item_image(item)

        holder.list.append(item)

        bind_item_instance_function(item, holder, h_index)

        if holder == vars.deck:  # Deck specific for now
            item.gui_button.configure(command=lambda c=item: move_item(c, vars.deck, vars.active_row))
            # item_index = holder.list.index(item)
            # item.gui_button.grid(row=math.floor(item_index / 3), column=item_index % 3, padx=2, pady=2)


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

        elif new_holder == vars.deck:
            item.gui_button.configure(command=lambda c=item: move_item(c, vars.deck, vars.active_row),
                                      compound=tk.NONE)

        item.gui_button.bind('<Button-2>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-2 on Mac
        item.gui_button.bind('<Button-3>', lambda event, c=item: show_big_card(event, c))  # r-click is Button-3 on PC

def activate_cards():
    # rows is a dict of all item rows. Alongside other things in vars, it fully encompasses the game state (or should)
    rows = {'active': vars.active_row,
            'particle': vars.particle_row,
            'power': vars.power_row,}

    print('\nCard order:', vars.active_row.list)

    print('\n--------START--------')
    print('Granting 1 power token from the grid')
    create_item('Power', vars.power_row)

    for card in vars.active_row.list:
        for token in vars.particle_row.list.copy():
            # token.function(rows, root)
            vars.stack.append(vars.StackEvent(token, token.function, (rows, root)))
        for token in vars.power_row.list.copy():  # Use .copy() to solve index issues w/ removing tokens while looping
            # token.function(rows, root)
            vars.stack.append(vars.StackEvent(token, token.function, (rows, root)))

        vars.stack.append(vars.StackEvent(card, card.function, (rows, root)))
        # card.function(rows, root)

        while vars.stack:  # While the stack is not empty
            event = vars.stack.popleft()

            if 'computer' in event.origin.tags:
                print('Computer! Yay')
                # vars.stack.appendleft(vars.StackEvent(card, card.function, (rows, root)))


            # Base observer (debug)
            event.execute()


    print('---------END---------')

def update_deck_display():
    for card in vars.deck.list:
        deck_index = vars.deck.list.index(card)
        card.gui_button.grid(row=math.floor(deck_index / 3), column=deck_index % 3, padx=2, pady=2)

    root.after(100, update_deck_display)


def update_active_row_display(repeat=True):
    # Show the max # of tokens you can have
    active_row_label.configure(text=f'ACTIVE ROW ({len(vars.active_row.list)}/{vars.active_row.max_length})')

    for card in vars.active_row.list:
        card.gui_button.grid(row=1, column=vars.active_row.list.index(card))

        # Update token string
        if card.power_slots != 0:
            card.token_string = '(P)'*card.power_tokens + '( )'*(card.power_slots - card.power_tokens)

        # Update card status string to reflect any changes.
        card.gui_button.configure(text=card.status_string())

    if repeat:
        root.after(100, update_active_row_display)


def update_particle_row_display(repeat=True):
    for token in vars.particle_row.list:
        token.gui_button.grid(row=1, column=vars.particle_row.list.index(token))

    if repeat:
        root.after(100, update_particle_row_display)


def update_power_row_display(repeat=True):
    # Show the max # of tokens you can have
    power_row_label.configure(text=f'POWER TOKENS ({len(vars.power_row.list)}/{vars.power_row.max_length})')

    for token in vars.power_row.list:
        token.gui_button.grid(row=1, column=vars.power_row.list.index(token))


    if repeat:
        root.after(100, update_power_row_display)


def update_stat_display():
    stat_display_label.config(text=f'SCORE: {vars.score}  |  DATA:  {vars.data}')
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

    vars.deck.gui_frame = F_internal_deck_frame

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
    active_row_label.grid(row=0, column=0, columnspan=vars.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                        sticky=tk.W + tk.S + tk.E)
    vars.active_row.gui_frame = F_active_row

    # Particle token row
    F_particle_row = ttk.Frame(root, height=140)
    F_particle_row.grid(row=1, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)
    particle_row_label = ttk.Label(F_particle_row, text='PARTICLE TOKENS')
    particle_row_label.grid(row=0, column=0, columnspan=vars.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                          sticky=tk.W + tk.S + tk.E)
    vars.particle_row.gui_frame = F_particle_row

    # Power token row
    F_power_row = ttk.Frame(root, height=140)
    F_power_row.grid(row=2, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W + tk.E + tk.N)
    power_row_label = ttk.Label(F_power_row, text='POWER TOKENS')
    power_row_label.grid(row=0, column=0, columnspan=vars.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                          sticky=tk.W + tk.S + tk.E)
    vars.power_row.gui_frame = F_power_row

    # Controls
    F_controls = ttk.Frame(root)
    F_controls.grid(row=3, column=1, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.E + tk.W + tk.S)
    controls_label = ttk.Label(F_controls, text='CONTROLS')
    controls_label.grid(row=0, column=0, columnspan=vars.active_row.max_length, padx=5, pady=5, ipadx=1, ipady=1,
                        sticky=tk.W + tk.S + tk.E)

    booster_button = ttk.Button(F_controls, text='Open Booster', command=crack_booster_pack, takefocus=False)
    booster_button.grid(row=1, column=0)

    activate_cards_button = ttk.Button(F_controls, text='Activate Cards', command=activate_cards, takefocus=False)
    activate_cards_button.grid(row=1, column=1)

    card_sampler_button = ttk.Button(F_controls, text='Get 1 of Each Card', command=get_all_cards, takefocus=False)
    card_sampler_button.grid(row=1, column=2)

    vars.do_slow_activation = tk.IntVar()
    slow_activate_checkbox = ttk.Checkbutton(F_controls, variable=vars.do_slow_activation, takefocus=False,
                                            text= 'Press space to advance activation   ')
    slow_activate_checkbox.grid(row=1, column=3)

    root.after(0, update_stat_display)
    root.after(0, update_deck_display)
    root.after(0, update_active_row_display)
    root.after(0, update_particle_row_display)
    root.after(0, update_power_row_display)

    # create_item('Power', vars.deck)
    # create_item('e- Neutrino', vars.particle_row)
    # create_item('Muon Neutrino', vars.particle_row)
    # create_item('Tau Neutrino', vars.particle_row)

    root.mainloop()
