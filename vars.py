import tkinter as tk

# To solve circular import issues, this is a module where all the floating variables live
# There is surely a much better way to do this.

# class CardHolder:
#     def __init__(self, contents=[], max_size=999):
#         self.contents = contents
#         self.max_size = max_size

do_slow_activation = None  # Will eventually be a tkinter IntVar

neutrino_flux = 1000  # Should vary by week in actual version, pulled from actual data

data = 0
score = 0


class CardHolder:
    def __init__(self, max_length=-1, gui_frame=None):
        self.list = []  # In theory, could be better to have CardHolder inherit from list
        self.max_length = max_length
        self.active_index = -1

        self.gui_frame = gui_frame

# Set up our cardholders, which are jsut the places that cards go
deck = CardHolder()
active_row = CardHolder(max_length=6)
power_row = CardHolder(max_length=5)


# Card rarity coefficients. Used when opening booster packs.

# Keep in mind that the "true" rarity of any type is equal to the rarity coefficient times the number of cards of that
# rarity. So if you don't make many legendary cards, they will be getting hit twice.
r_common = 10
r_uncommon = 5
r_rare = 3
r_legendary = 1
