import tkinter as tk
from collections import deque

# To solve circular import issues, this is a module where all the floating variables live
# There is surely a much better way to do this.

do_slow_activation = None  # Becomes a tkinter IntVar at runtime

neutrino_flux = 1000  # Should vary by week in actual version, pulled from actual data

data = 0
score = 0

class StackEvent:
    def __init__(self, origin, function, f_args, tags=None):
        """
        Constructor.

        Args:
            origin: The object (usually a card/token) that the StackEven came from.
            function: The function associated with the StackEvent. The main observer will execute this.
            f_args: Arguments to be passed to the function.
            tags: Currently unused.
        """

        self.origin = origin
        self.function = function
        self.f_args = f_args
        self.tags = tags

    # def execute(self):
    #     self.function(*self.f_args)  # Remember to unpack the args

stack = deque([])

observers = deque([])  # Deque that contains all the observers. Main observer goes on first, then append additional ones

class Observer:
    # Observers are objects that process StackEvents. There is one main observer that executes card/token functions
    # and some number of additional observers that implement passive effects. Anything that needs to modify a stack
    # event or be triggered by a stack event is handled by Observers.
    def __init__(self, function, f_args=None):
        """
        Constructor.

        Args:
            function: The function the observer will execute. Must always take the event as the first argument.
            f_args: If the function needs any additional args, put them here. Not implemented right now.
        """
        self.function = function

# Main observer, executes the function listed on the card/token
def f_main_observer(event):
    event.function(*event.f_args)
main_observer = Observer(f_main_observer)
observers.append(main_observer)


# # I fear this all is very stupid
# def do_card_function(stack_event):
#     stack_event.execute()
# main_observer = Observer(do_card_function)


class CardHolder:
    def __init__(self, max_length=-1, gui_frame=None):
        self.list = []  # In theory, could be better to have CardHolder inherit from list
        self.max_length = max_length
        self.active_index = -1

        self.gui_frame = gui_frame

# Set up our cardholders, which are just the places that cards go
deck = CardHolder()
active_row = CardHolder(max_length=6)
particle_row = CardHolder()
power_row = CardHolder(max_length=5)


# Card rarity coefficients. Used when opening booster packs.

# Keep in mind that the "true" rarity of any type is equal to the rarity coefficient times the number of cards of that
# rarity. So if you don't make many legendary cards, they will be getting hit twice.
r_common = 10
r_uncommon = 5
r_rare = 3
r_legendary = 1
