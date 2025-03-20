import vars
import tkinter as tk
from copy import deepcopy
import time

def allocate_power_tokens(index, active_row):
    """Allocate as many unused power tokens as possible to active powered cards with indices > index."""
    for card in active_row[index+1:]:
        tokens_added = 0  # Internal, just for debug / console message printing
        for _ in range(card.power_slots - card.power_tokens):
            card.power_tokens += 1
            tokens_added += 1
            vars.unused_power_tokens -= 1
            if vars.unused_power_tokens == 0:
                break
        if tokens_added > 0:
            print(f'Allocated {tokens_added} power token(s) to {active_row.index(card)} {card}!')

            # card.gui_button.configure(text='(P)'*card.power_tokens, compound=tk.TOP)
        if vars.unused_power_tokens == 0:
            print('All power tokens allocated!')
            break

# Contains the general card_name class and the special functions for invoking each card_name.

# f stands for function
def f_default():
    """Default card_name function as a fallback."""
    raise Exception('Card activated with undefined function')

def f_start(self, ar, root):
    """Perform functions universal to all cards at activation start."""
    self.gui_button.configure(text='ACTIVE', compound=tk.TOP)
    root.update()
    pass

def f_end(self, ar, root):
    """Perform functions universal to all cards at activation end."""

    def wait_for_spacebar():
        spacebar_pressed = False

        def _on_spacebar(event):
            nonlocal spacebar_pressed
            spacebar_pressed = True

        root.bind("<space>", _on_spacebar)

        while not spacebar_pressed:
            root.update()
            root.update_idletasks()
            pass

    if vars.do_slow_activation.get():
        wait_for_spacebar()
    else:
        time.sleep(1)

    self.gui_button.configure(text='', compound=tk.NONE)
    root.update()
    pass







def f_icecube(self, ar, root):
    """Generate data from neutrino flux."""
    f_start(self, ar, root)
    vars.data += vars.neutrino_flux
    print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux}!')
    f_end(self, ar, root)

def f_super_kamiokande(self, ar, root):
    """Generate data from neutrino flux, more efficiently if the neutrino oscillation card is in the active row."""
    f_start(self, ar, root)
    if 'Neutrino Oscill.' in [card.name for card in ar]:
        vars.data += vars.neutrino_flux * 1.5
        print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux * 1.5}! (More efficient due to '
              f'neutrino oscillation card)')
    else:
        vars.data += vars.neutrino_flux * 0.8
        print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux * 0.8}!')
    f_end(self, ar, root)


# Prototype functions for the initial demo / testing
def f_retrigger_left(self, ar, root):
    """Re-activate the ability of the card_name to the left."""
    f_start(self, ar, root)
    active_row = ar
    my_index = active_row.index(self)  # The index of this retrigger card

    if my_index == 0:
        print(f'{ar.index(self)} {self.name}:\tNo card found to the left!')
    else:
        print(f'{ar.index(self)} {self.name}:\tRe-activating card to the left!')
        active_row[active_row.index(self) - 1].function(active_row, root)  # I don't like passing the active row every time.
    f_end(self, ar, root)

def f_neutrino_generator(self, ar, root):
    """Increase the current neutrino flux."""
    f_start(self, ar, root)
    vars.neutrino_flux += 500
    print(f'{ar.index(self)} {self.name}:\tIncreased Neutrino Flux by 500 (flux is now {vars.neutrino_flux}).')
    f_end(self, ar, root)


def f_machine_learning(self, ar, root):
    """Generate score from data based on the card's current multiplier, then increase the multiplier."""
    f_start(self, ar, root)
    if self.power_tokens == 0: # Card requires 1 token to run
        print(f'{ar.index(self)} {self.name}:\tUnpowered!')
    else:
        # Increase score
        score_increase = vars.data * self.param
        vars.score += score_increase

        for card in ar:
            if 'computer' in card.tags:  # Perma-increase multiplier by the number of computer cards in your row
                self.param += 0.1
            self.param = round(self.param, 2)

        print(f'{ar.index(self)} {self.name}:\tGenerated {score_increase} score from {vars.data} data! '
              f'ML multiplier increased to {self.param}.')
    f_end(self, ar, root)

def f_recompute(self, ar, root):
    """Re-activate all cards with the 'computer' tag."""
    f_start(self, ar, root)
    for card in ar:
        if 'computer' in card.tags:
            print(f'{ar.index(self)} {self.name}:\tRe-activating {ar.index(card)} {card.name} due to its computer tag!')
            card.function(ar, root)
    f_end(self, ar, root)

def f_fission_reactor(self, ar, root):
    f_start(self, ar, root)
    vars.neutrino_flux += 1000
    print(f'{ar.index(self)} {self.name}\t: Increased Neutrino Flux by 1000 (flux is now {vars.neutrino_flux}).')

    vars.unused_power_tokens += 5
    print(f'{ar.index(self)} {self.name}\t: Added 5 power tokens to the pool! Attempting to allocate power to cards...')

    i = ar.index(self)
    allocate_power_tokens(i, ar)
    f_end(self, ar, root)


def f_lbnf_beam(self, ar, root):
    f_start(self, ar, root)
    if self.power_tokens == 0: # Card requires at least 1 token to run
        print(f'{ar.index(self)} {self.name}:\tUnpowered!')
    else:
        vars.neutrino_flux += 1000 * self.power_tokens
        print(f'{ar.index(self)} {self.name}\t: Increased Neutrino Flux by {1000 * self.power_tokens} '
              f'(flux is now {vars.neutrino_flux}).')
    f_end(self, ar, root)

def f_neutrino_oscillation(self, ar, root):
    f_start(self, ar, root)
    print(f'{ar.index(self)} {self.name}\t: Multiplying score for each [neutrino] card...')
    for card in ar:
        if 'neutrino' in card.tags:
            vars.score = vars.score * 1.5
            print(f'{ar.index(self)} {self.name}\t: Multiplied score by 1.5 due to {ar.index(card)} {card.name}`s '
                  f'[neutrino] tag! Score is now {vars.score}!')
    f_end(self, ar, root)
    # TODO: As mentioned on the card, come up with a cooler name for this

class Card:
    """The general class used for each card in the game."""
    def __init__(self, name='', image_file=None, card_type='', tags=(), function=f_default, param=0.0,
                 rarity=vars.r_common, power_slots=0, power_tokens=0):
        self.name = name
        self.image_file = image_file

        self.card_type = card_type
        self.tags = tags
        self.rarity = rarity  # Coefficient to weight draw rarity. Higher number = more common card.

        self.param = param

        self.power_slots = power_slots  # The max number of power tokens that can be on the card
        self.power_tokens = power_tokens  # The number of power tokens that are on the card. Generally starts at 0

        self.function = function

        self.gui_button = None

    def __repr__(self):
        return self.name


def card_factory(card_name):
    """Factory method."""

    global card_dict

    return deepcopy(card_dict[card_name])


# Huge master dict of all the cards and their effects.
card_dict = {
    # Prototype Cards
    'Neutrino Gen':     Card(name='Neutrino Gen', card_type='prototype', tags=['neutrino'],
                             image_file='small_card_images/fp_small_neutrino_gen.png',
                             rarity=vars.r_uncommon, function=f_neutrino_generator),
    'ReCompute':        Card(name='ReCompute', card_type='prototype',
                             image_file='small_card_images/fp_small_recompute.png',
                             rarity=vars.r_uncommon, function=f_recompute),
    'Re-Trigger':       Card(name='Re-Trigger', card_type='prototype',
                             image_file='small_card_images/fp_small_retrigger.png',
                             rarity=vars.r_uncommon, function=f_retrigger_left),

    # Detector Cards
    'IceCube':          Card(name='IceCube', card_type='detector', tags=['neutrino', 'astro'],
                             image_file='small_card_images/fp_small_icecube.png', function=f_icecube),
    'SuperKamiokande':  Card(name='SuperKamiokande', card_type='detector', tags=['neutrino', 'astro'],
                             image_file='small_card_images/fp_small_sk.png', function=f_super_kamiokande),

    # Analysis Cards
    'Machine Learning': Card(name='Machine Learning', card_type='analysis', tags=['computer'],
                             image_file='small_card_images/fp_small_ml.png', param=0.8, power_slots=1,
                             function=f_machine_learning),

    # Special Cards
    'Fission Reactor':  Card(name='Fission Reactor', card_type='special', tags=['reactor', 'neutrino'],
                             image_file='small_card_images/fp_small_fission_reactor.png', rarity=vars.r_uncommon,
                             function=f_fission_reactor),
    'LBNF Beam':        Card(name='LBNF Beam', card_type='special', tags=['beam', 'neutrino'],
                             image_file='small_card_images/fp_small_lbnf_beam.png', power_slots=3,
                             function=f_lbnf_beam),

    # Physics Cards (temporary name)
    'Neutrino Oscill.': Card(name='Neutrino Oscill.', card_type='physics', tags=['neutrino'],
                             image_file='small_card_images/fp_small_neutrino_oscillation.png', rarity=vars.r_rare,
                             function=f_neutrino_oscillation),

    }
