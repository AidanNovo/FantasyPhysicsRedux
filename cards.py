import vars
from copy import deepcopy

# Contains the general card_name class and the special functions for invoking each card_name.

# f stands for function
def f_default():
    """Default card_name function as a fallback."""
    raise Exception('Card activated with undefined function')


class Card:
    """A class for the general card_name object. Specific card_dict inherit from this."""

    def __init__(self, name='', image=None, card_type='', tags=(), function=f_default, param=0.0):
        self.name = name
        self.image = image

        self.card_type = card_type
        self.tags = tags
        self.function = function

        self.param = param  # Mostly for testing purposes as a general-purpose card parameter. Tracks ML mult, for example

    def __repr__(self):
        return self.name


def f_icecube(self, ar):
    """Generate data from neutrino flux."""
    active_row = ar
    vars.data += vars.neutrino_flux
    print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux}!')

# Prototype functions for the initial demo / testing
def f_retrigger_left(self, ar):
    """Re-activate the ability of the card_name to the left."""

    active_row = ar
    my_index = active_row.index(self)  # The index of this retrigger card

    if my_index == 0:
        print(f'{ar.index(self)} {self.name}:\tNo card found to the left!')
    else:
        print(f'{ar.index(self)} {self.name}:\tRe-activating card to the left!')
        active_row[active_row.index(self) - 1].function(active_row)  # I don't like passing the active row every time.


def f_neutrino_generator(self, ar):
    """Increase the current neutrino flux."""
    vars.neutrino_flux += 500
    print(f'{ar.index(self)} {self.name}:\tIncreased Neutrino Flux by 500 (flux is now {vars.neutrino_flux}).')


def f_machine_learning(self, ar):
    """Generate score from data based on the card's current multiplier, then increase the multiplier."""
    score_increase = vars.data * self.param
    vars.score += score_increase

    for card in ar:
        if 'computer' in card.tags:  # Perma-increase multiplier by the number of computer cards in your row
            self.param += 0.1

    print(f'{ar.index(self)} {self.name}:\tGenerated {score_increase} score from {vars.data} data! '
          f'ML multiplier increased to {self.param}.')


def f_recompute(self, ar):
    """Re-activate all cards with the 'computer' tag."""
    for card in ar:
        if 'computer' in card.tags:
            print(f'{ar.index(self)} {self.name}:\tRe-activating {ar.index(card)} {card.name} due to its computer tag!')
            card.function(ar)


def card_factory(card_name):
    """Factory Method (I think)"""

    global card_dict

    return deepcopy(card_dict[card_name])


# Huge master dict of all the cards and their effects.
card_dict = {
    # Prototype Cards
    'Neutr. Gen':   Card(name='Neutr. Gen', card_type='prototype', tags=['neutrino'],
                         image='fp_small_neutrino_gen.png', function=f_neutrino_generator),
    'ReCompute':    Card(name='ReCompute', card_type='prototype',
                         image='fp_small_recompute.png', function=f_recompute),
    'Re-Trigger':   Card(name='Re-Trigger', card_type='prototype',
                         image='fp_small_retrigger.png', function=f_retrigger_left),


    # Detector Cards
    'IceCube':      Card(name='IceCube', card_type='detector', tags=['neutrino', 'astro'],
                         image='fp_small_icecube.png', function=f_icecube),

    # Analysis Cards
    'Mach. Lrn.':   Card(name='Mach. Lrn.', card_type='analysis', tags=['computer'],
                         image='fp_small_ml.png', function=f_machine_learning, param=0.8),

    # Auxiliary Cards

    }
