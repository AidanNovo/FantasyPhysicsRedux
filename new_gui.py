import customtkinter as ctk
import math

import common
from common import root_instance


# This module exists for organizational reasons, to split all the tkinter code (or most of it) off into its own place.

# TODO: Consider further organizing the GUI code by implementing functions that create distinct GUI elements.
#  e.g. create_sidebar() that initializes all the sidebar code.
#  That said, I am not sure this will help. May just add in a layer of bloat.


def update_deck_display():
    """Update the deck display to reflect the current deck state."""
    for card in common.deck.list:
        deck_index = common.deck.list.index(card)

        card.gui_button.grid(row=math.floor(deck_index / 3), column=deck_index % 3, padx=2, pady=2)

    root.after(100, update_deck_display)


def update_active_row_display(repeat=True):
    """Update the active row display to reflect the current active row state."""
    # Show the max # of tokens you can have
    root.CardRows.active_row_label.configure(text=f'ACTIVE ROW ({len(common.active_row.list)}/{common.active_row.max_length})')
    # active_row_label.configure(text=f'ACTIVE ROW ({len(common.active_row.list)}/{common.active_row.max_length})')

    for card in common.active_row.list:
        card.gui_button.grid(row=1, column=common.active_row.list.index(card), padx=2, pady=5)

        # Update token string
        if card.power_slots != 0:
            card.token_string = '(P)'*card.power_tokens + '( )'*(card.power_slots - card.power_tokens)

        # Update card status string to reflect any changes.
        card.gui_button.configure(text=card.status_string())

    if repeat:
        root.after(100, update_active_row_display)


def update_particle_row_display(repeat=True):
    """Update the particle row display to reflect the current particle row state."""
    for token in common.particle_row.list:
        token.gui_button.grid(row=1, column=common.particle_row.list.index(token), padx=2, pady=5)

    if repeat:
        root.after(100, update_particle_row_display)


def update_power_row_display(repeat=True):
    """Update the power row display to reflect the current power row state."""
    # Show the max # of tokens you can have
    root.CardRows.power_row_label.configure(text=f'POWER TOKENS ({len(common.power_row.list)}/{common.power_row.max_length})')

    for token in common.power_row.list:
        token.gui_button.grid(row=1, column=common.power_row.list.index(token), padx=2, pady=5)


    if repeat:
        root.after(100, update_power_row_display)


def update_stat_display():
    """Update the stat display to reflect the current game state."""
    root.Sidebar.stat_display_label.configure(text=f'SCORE: {common.score}  |  DATA:  {common.data}')
    # stat_display_label.configure(text=f'SCORE: {common.score}  |  DATA:  {common.data}')
    root.after(100, update_stat_display)


class Root(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(padx=40, pady=40)

        self.title('FantasyPhysics')
        self.geometry('1000x600')
        self.grid_columnconfigure(0, minsize=400)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.Sidebar = SideBarFrame(self)
        self.Sidebar.grid(column=0, row=0, rowspan=2, sticky='nswe', padx=(0, 5))

        self.CardRows = CardRowsFrame(self)
        self.CardRows.grid(column=1, row=0, sticky='nswe')

        self.ControlPanel = ControlPanelFrame(self)
        self.ControlPanel.grid(column=1, row=1, sticky='we', pady=(5, 0))


class SideBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.deck_list_label = ctk.CTkLabel(self, text='DECK LIST')
        self.deck_list_label.grid(column=0, row=0, sticky='we')

        self.deck_display_frame = ctk.CTkScrollableFrame(self)
        self.deck_display_frame.grid(column=0, row=1, sticky='nswe')
        # Make all three columns space themselves evenly
        self.deck_display_frame.grid_columnconfigure(0, weight=1)
        self.deck_display_frame.grid_columnconfigure(1, weight=1)
        self.deck_display_frame.grid_columnconfigure(2, weight=1)
        common.deck.gui_frame = self.deck_display_frame
        # common.interpreters.gui_frame = self.deck_display_frame  # Debug code


        self.stat_display_label = ctk.CTkLabel(self, text='SCORE: 0')
        self.stat_display_label.grid(column=0, row=2, sticky='we')


# class DeckDisplayFrame(ctk.CTkScrollableFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#
#         common.deck.gui_frame = self


class CardRowsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        # self.configure(fg_color='transparent', border_width=0)

        # PARTICLE ROW
        self.particle_row_label = ctk.CTkLabel(self, text='PARTICLE TOKENS', anchor='w')
        self.particle_row_label.grid(column=0, row=0, sticky='we', pady=(5, 0))
        #
        # self.particle_row_graphic = ctk.CTkFrame(self, border_width=4, height=10)
        # self.particle_row_graphic.grid(column=0, row=1, sticky='we', pady=(0, 0), rowspan=2)

        self.particle_row_frame = ctk.CTkFrame(self)
        self.particle_row_frame.grid(column=0, row=2, sticky='we', pady=(0, 5))
        common.particle_row.gui_frame = self.particle_row_frame

        # POWER ROW
        self.power_row_label = ctk.CTkLabel(self, text='POWER TOKENS', anchor='w')
        self.power_row_label.grid(column=0, row=3, sticky='we', pady=(5, 0))

        self.power_row_frame = ctk.CTkFrame(self)
        self.power_row_frame.grid(column=0, row=4, sticky='we', pady=(0, 5))
        common.power_row.gui_frame = self.power_row_frame

        # ACTIVE ROW
        self.active_row_label = ctk.CTkLabel(self, text='ACTIVE ROW', anchor='w')
        self.active_row_label.grid(column=0, row=5, sticky='we', pady=(5, 0))

        self.active_row_frame = ctk.CTkFrame(self)
        self.active_row_frame.grid(column=0, row=6, sticky='we', pady=(0, 5))
        common.active_row.gui_frame = self.active_row_frame


class ControlPanelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        from main import crack_booster_pack
        self.crack_booster_button = ctk.CTkButton(self, text='Crack Booster', command=crack_booster_pack)
        self.crack_booster_button.grid(column=0, row=0, padx=5, pady=5)

        from main import activate_cards
        self.activate_cards_button = ctk.CTkButton(self, text='Activate Cards', command=lambda: activate_cards(root))
        self.activate_cards_button.grid(column=1, row=0, padx=5, pady=5)

        from main import get_all_cards
        self.get_all_cards_button = ctk.CTkButton(self, text='Get 1 of Each Card', command=get_all_cards)
        self.get_all_cards_button.grid(column=2, row=0, padx=5, pady=5)

        common.do_slow_activation = ctk.BooleanVar()  # Have to do this here
        slow_activate_checkbox = ctk.CTkCheckBox(self, variable=common.do_slow_activation,
                                                 text='Press space to advance activation')
        slow_activate_checkbox.grid(column=3, row=0, padx=5, pady=5)

class BigItemDisplay(ctk.CTkToplevel):
    def __init__(self, master, item):
        super().__init__(master)
        self.resizable(False, False)
        self.title(item.name)
        self.image_label = ctk.CTkLabel(self, image=item.large_image, text='')
        self.image_label.pack()


def get_root():
    if common.root_instance is None:
        common.root_instance = Root()  # Create only once
    return common.root_instance

if __name__ == '__main__':
    ctk.set_default_color_theme('fp_theme.json')
    root = get_root()

    # This needs to be in here to make sure the interpreter does not get initialized too early (tkinter sucks)
    from main import create_item
    create_item('Main Interpreter', common.interpreters)

    root.after(0, update_stat_display)
    root.after(0, update_deck_display)
    root.after(0, update_active_row_display)
    root.after(0, update_particle_row_display)
    root.after(0, update_power_row_display)

    root.mainloop()
