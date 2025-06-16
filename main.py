import random
import tkinter as tk
from PIL import Image, ImageTk

import cards
import common

# This module exists to contain the main functions related to the game's logic. Things from gui.py will be calling these
# functions, in theory.

# TODO: Implement a GUI to reorganize your active row
# TODO: Implement a basic score attack mode (ala Balatro, Nubby, Luck be a Landlord, etc.)
# TODO: Implement outreach scaling
# TODO: Organize these modules better
# TODO: Look into moving some of these functions into common.py or gui.py


def crack_booster_pack(pack_size=5,
                       draw_pool=tuple(cards.card_dict.keys()),
                       draw_weights=tuple(int(cards.card_dict[c].rarity) for c in cards.card_dict.keys())):
    """Add n randomly chosen cards to the deck, weighted by rarity, with replacement.

    Args:
        pack_size: The number of cards to draw and add to the deck.
        draw_pool: A tuple of cards.card_dict keys comprising the pool to pick cards from. Defaults to all cards.
        draw_weights: The weights to draw cards with. Must be the same size as draw_pool.
    """

    print('Opening a booster pack...')

    pulled_cards = random.choices(population=draw_pool, weights=draw_weights, k=pack_size)

    for c in pulled_cards:
        print(f'You found a(n) {c} card!')
        create_item(c, holder=common.deck)

    print('Deck:', common.deck.list)


def get_all_cards():
    """Add one copy of each card in card_dict to the deck."""
    for card_name in cards.card_dict.keys():
        create_item(card_name, holder=common.deck)


def show_big_item(event, item):
    """Create a window displaying a larger version of an item.

    Args:
        event: The mouse-click event passed to this function by tkinter.
        item: The card/token/etc object to be displayed.
    """

    popup = tk.Toplevel(common.root)
    big_image = item.large_image
    image_label = tk.Label(popup, image=big_image)
    image_label.pack()


def initialize_item_gui_button(item, holder):
    """Initialize an item's gui button and bind the right-click functionality.

    Args:
        item: The item being initialized.
        holder: The CardHolder which the item is being initialized into.
    """

    item.gui_button = tk.Button(holder.gui_frame)
    item.gui_button.bind('<Button-2>', lambda event, c=item: show_big_item(event, c))  # r-click is Button-2 on Mac
    item.gui_button.bind('<Button-3>', lambda event, c=item: show_big_item(event, c))  # r-click is Button-3 on PC


def initialize_item_image(item):
    """Initialize the various images for the item."""
    base_img = Image.open(item.image_file)
    item.image = ImageTk.PhotoImage(base_img.resize((100, 140)))
    item.large_image = ImageTk.PhotoImage(base_img.resize((250, 350)))

    item.gui_button.configure(image=item.image)


def bind_item_instance_function(item, holder, h_index):
    """Bind an item's main and prerun functions to the specific instance being initialized.

    Note that this function must be called *after* the item is appended into its CardHolder.

    Args:
        item: The item being initialized.
        holder: The CardHolder which the item is being initialized into.
        h_index: The item's index in its CardHolder.
    """
    # To be honest, I do not fully understand this code, but it is very important.

    # Bind the instance method
    holder.list[h_index].function = holder.list[h_index].function.__get__(holder.list[h_index], type(item))

    # Bind the prerun function method (if needed)
    if item.prerun_function is not None:
        holder.list[h_index].prerun_function = holder.list[h_index].prerun_function.__get__(holder.list[h_index], type(item))


def create_item(item_name, holder, h_index=-1):
    """Create an item, append it to its holder, and bind the item's function to the instance created.

    Args:
        item_name: The name of the item to be created. Must be a key in cards.card_dict or cards.token_dict.
        holder: The CardHolder which the item is being initialized into.
        h_index: The item's index in its CardHolder. Defaults to -1, which is the end of the list.
    """

    if len(holder.list) == holder.max_length:
        print(f'Could not add item to {holder}.')

    else:
        # Create the item object
        item = cards.item_factory(item_name)

        initialize_item_gui_button(item, holder)

        initialize_item_image(item)

        holder.list.append(item)

        bind_item_instance_function(item, holder, h_index)

        # If the item is being initialized into the deck, bind the move_item function to the item's gui button.
        if holder == common.deck:
            item.gui_button.configure(command=lambda c=item: move_item(c, common.deck, common.active_row))


def move_item(item, old_holder, new_holder):
    """Move an item from one CardHolder to another.

    Args:
        item: The item to be moved.
        old_holder: The CardHolder which the item is being moved from.
        new_holder: The CardHolder which the item is being moved to.
    """

    if len(new_holder.list) == new_holder.max_length:
        print(f'Could not add item to {new_holder}.')
    else:
        cfg = item.gui_button.config()
        item.gui_button.destroy()

        old_index = old_holder.list.index(item)
        new_holder.list.append(old_holder.list.pop(old_index))

        item.gui_button = tk.Button(new_holder.gui_frame, image=cfg['image'][4], compound=tk.TOP)

        if new_holder == common.active_row:
            item.gui_button.configure(command=lambda c=item: move_item(c, common.active_row, common.deck),
                                      compound=tk.TOP)

        elif new_holder == common.deck:
            item.gui_button.configure(command=lambda c=item: move_item(c, common.deck, common.active_row),
                                      compound=tk.NONE)

        item.gui_button.bind('<Button-2>', lambda event, c=item: show_big_item(event, c))  # r-click is Button-2 on Mac
        item.gui_button.bind('<Button-3>', lambda event, c=item: show_big_item(event, c))  # r-click is Button-3 on PC


def activate_cards(root):
    """Activate all cards in the active row.

    This is the function that contains the main game logic. Note that we pass root (the tkinter root) as an argument
    just so that f_card_start and f_card_end can update the text display on card tokens.

    Args:
        root: The tkinter root.
    """

    # Rows is a dict of all item rows.
    rows = {'active': common.active_row,
            'particle': common.particle_row,
            'power': common.power_row, }

    print('\nCard order:', common.active_row.list)  # For debugging purposes

    print('\n------PASSIVES-------')
    # Process all prerun functions. Note that they are not put on a stack
    # TODO: Handle prerun functions with a stack.
    for card in common.active_row.list:
        if card.prerun_function is not None:
            card.prerun_function(rows, root)

    print('\n--------START--------')
    print('Granting 1 power token from the grid')
    create_item('Power', common.power_row)


    # We handle activating card and token abilities with a stack.
    #
    # The current card's activation and all token activations are placed into the stack, then we pop them off the top
    # until the stack is empty. When an activation is popped off the stack, it is passed to each Interpreter in
    # common.interpreters (in order), which do various things depending on the activation's attributes. The last
    # Interpreter executes the function associated with the StackEvent.
    #
    # Then, we go on to the next card and repeat.

    for card in common.active_row.list:
        # Fill up the stack...
        common.stack.append(common.StackEvent(card, card.function, (rows, root)))

        for token in reversed(common.power_row.list):  # Reversed to fill the stack in a user-intuitive order (L->R)
            common.stack.append(common.StackEvent(token, token.function, (rows, root)))

        for token in reversed(common.particle_row.list):
            common.stack.append(common.StackEvent(token, token.function, (rows, root)))

        # ...then empty the stack.
        while common.stack:  # While the stack is not empty
            event = common.stack.pop()

            # Use list() to 'freeze' the interpreters deque and prevent a RuntimeError.
            for interpreter in list(common.interpreters):
                interpreter.function(event)

    print('---------END---------')
