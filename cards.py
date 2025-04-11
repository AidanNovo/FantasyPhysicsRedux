import vars
import tkinter as tk
from copy import deepcopy
# from main import create_item
import time

# f stands for function
def f_default():
    """Default function as a fallback."""
    raise Exception('Card/token activated with undefined function')

def f_card_start(self, ar, root):
    """Perform functions universal to all cards at activation start."""
    self.activity_string = 'ACTIVE'
    ar.active_index = ar.list.index(self)
    # print('ai', ar.active_index)
    self.gui_button.configure(text=self.status_string(), compound=tk.TOP)
    root.update()
    pass

def f_card_end(self, ar, root):
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

    self.activity_string = '--'
    self.gui_button.configure(text=self.status_string(), compound=tk.TOP)
    root.update()
    pass

def f_t_test(self, ar, pr, root):
    print('token activated')


class Item:
    def __init__(self, name='', image_file=None, function=f_default, item_type='', tags=(),):
        self.name = name
        self.image_file = image_file
        self.function = function
        self.item_type = item_type
        self.tags = tags

    def __repr__(self):
        return self.name


class Card(Item):
    """The general class used for each card in the game."""
    def __init__(self, rarity=vars.r_common, param=0.0, power_slots=0, power_tokens=0, **kwargs):
        super().__init__(**kwargs)
        self.rarity = rarity  # Coefficient to weight draw rarity. Higher number = more common card.
        self.param = param
        self.power_slots = power_slots # The max number of power tokens that can be on the card
        self.power_tokens = power_tokens # The number of power tokens that are on the card. Generally starts at 0

        self.token_string = '[no tokens]'  # For testing/demo. The string in which power tokens (if any) are displayed
        self.activity_string = '--'

        self.gui_button = None


    def status_string(self):
        """
        Return the card's status string.

        The status string is what gets displayed under the card in the active row.
        Includes whether the card is active, the token display, etc.
        """
        status_string = (f'{self.token_string}\n'
                         f'{self.activity_string}')

        return status_string


class Token(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def item_factory(item_name):
    """Factory method."""

    global card_dict
    global token_dict

    try:
        return deepcopy(card_dict[item_name])
    except KeyError:
        return deepcopy(token_dict[item_name])


# Huge master dict of all the cards and their effects.
card_dict = {}

# Analysis Cards
def f_machine_learning(self, rows, root):
    """Generate score from data based on the card's current multiplier, then increase the multiplier."""
    ar = rows['active']

    f_card_start(self, ar, root)
    if self.power_tokens == 0: # Card requires 1 token to run
        print(f'{ar.list.index(self)} {self.name}:\tUnpowered!')
    else:
        # Increase score
        score_increase = vars.data * self.param
        vars.score += score_increase

        for card in ar.list:
            if 'computer' in card.tags:  # Perma-increase multiplier by the number of computer cards in your row
                self.param += 0.1
            self.param = round(self.param, 2)

        print(f'{ar.list.index(self)} {self.name}:\tGenerated {score_increase} score from {vars.data} data! '
              f'ML multiplier increased to {self.param}.')
    f_card_end(self, ar, root)
card_dict.update({'Machine Learning': Card(
    name='Machine Learning', function=f_machine_learning, image_file='card_images/fp_machine_learning.png',
    item_type='analysis', tags=['computer'], param=0.8, power_slots=1)})


# Detector Cards
def f_icecube(self, rows, root):
    """Generate data from neutrino flux."""
    ar = rows['active']

    f_card_start(self, ar, root)
    vars.data += vars.neutrino_flux
    print(f'{ar.list.index(self)} {self.name}:\tData increased by {vars.neutrino_flux}!')
    f_card_end(self, ar, root)
card_dict.update({'IceCube': Card(
    name='IceCube', function=f_icecube, image_file='card_images/fp_icecube.png',
    item_type='detector', tags=['neutrino', 'astro'])})

def f_super_kamiokande(self, rows, root):
    """Generate data from neutrino flux, more efficiently if the neutrino oscillation card is in the active row."""
    ar = rows['active']

    f_card_start(self, ar, root)
    if 'Neutrino Oscill.' in [card.name for card in ar.list]:
        vars.data += vars.neutrino_flux * 1.5
        print(f'{ar.list.index(self)} {self.name}:\tData increased by {vars.neutrino_flux * 1.5}! (More efficient due to '
              f'neutrino oscillation card)')
    else:
        vars.data += vars.neutrino_flux * 0.8
        print(f'{ar.list.index(self)} {self.name}:\tData increased by {vars.neutrino_flux * 0.8}!')
    f_card_end(self, ar, root)
card_dict.update({'Super-Kamiokande': Card(
    name='Super-Kamiokande', function=f_super_kamiokande, image_file='card_images/fp_super_k.png',
    item_type='detector', tags=['neutrino', 'astro'])})


# Physics Cards (temporary name)
def f_neutrino_oscillation(self, rows, root):
    ar = rows['active']

    f_card_start(self, ar, root)
    print(f'{ar.list.index(self)} {self.name}\t: Multiplying score for each [neutrino] card...')
    for card in ar.list:
        if 'neutrino' in card.tags:
            vars.score = vars.score * 1.5
            print(f'{ar.list.index(self)} {self.name}\t: Multiplied score by 1.5 due to {ar.list.index(card)}'
                  f'{card.name}`s [neutrino] tag! Score is now {vars.score}!')
    f_card_end(self, ar, root)
    # TODO: As mentioned on the card, come up with a cooler name for this
card_dict.update({'Neutrino Oscillation': Card(
    name='Neutrino Oscillation', function=f_neutrino_oscillation, image_file='card_images/fp_neutrino_oscillation.png',
    item_type='physics', tags=['neutrino'], rarity=vars.r_rare)})


# Special Cards
def f_fission_reactor(self, rows, root):
    ar = rows['active']

    from main import create_item
    f_card_start(self, ar, root)
    vars.neutrino_flux += 1000
    print(f'{ar.list.index(self)} {self.name}\t: Increased Neutrino Flux by 1000 (flux is now {vars.neutrino_flux}).')

    for _ in range(5):  # Make 5 power tokens
        create_item('Power', vars.power_row)

    f_card_end(self, ar, root)
card_dict.update({'Fission Reactor': Card(
    name='Fission Reactor', function=f_fission_reactor, image_file='card_images/fp_fission_reactor.png',
    item_type='special', tags=['reactor', 'neutrino'], rarity=vars.r_uncommon)})

def f_lbnf_beam(self, rows, root):
    ar = rows['active']

    f_card_start(self, ar, root)
    if self.power_tokens == 0: # Card requires at least 1 token to run
        print(f'{ar.list.index(self)} {self.name}:\tUnpowered!')
    else:
        vars.neutrino_flux += 1000 * self.power_tokens
        print(f'{ar.list.index(self)} {self.name}\t: Increased Neutrino Flux by {1000 * self.power_tokens} '
              f'(flux is now {vars.neutrino_flux}).')
    f_card_end(self, ar, root)
card_dict.update({'LBNF Beam': Card(
    name='LBNF Beam', function=f_lbnf_beam, image_file='card_images/fp_lbnf_beam.png',
    item_type='special', tags=['beam', 'neutrino'], power_slots=3)})


# Prototype Cards
def f_neutrino_generator(self, rows, root):
    """Increase the current neutrino flux."""
    ar = rows['active']

    f_card_start(self, ar, root)
    vars.neutrino_flux += 500
    print(f'{ar.list.index(self)} {self.name}:\tIncreased Neutrino Flux by 500 (flux is now {vars.neutrino_flux}).')
    f_card_end(self, ar, root)
card_dict.update({'Neutrino Gen': Card(
    name='Neutrino Gen', function=f_neutrino_generator, image_file='card_images/fp_neutrino_gen.png',
    item_type='prototype', tags=['neutrino'], rarity=vars.r_uncommon)})

def f_recompute(self, rows, root):
    """Re-activate all cards with the 'computer' tag."""
    ar = rows['active']
    rr = rows['power']

    f_card_start(self, ar, root)
    for card in ar.list:
        if 'computer' in card.tags:
            print(f'{ar.list.index(self)} {self.name}:\tRe-activating {ar.list.index(card)} {card.name} due to its computer tag!')
            card.function(rows, root)
    f_card_end(self, ar, root)
card_dict.update({'ReCompute': Card(
    name='ReCompute', function=f_recompute, image_file='card_images/fp_recompute.png',
    item_type='prototype', rarity=vars.r_uncommon)})

def f_retrigger_left(self, rows, root):
    """Re-activate the ability of the item_name to the left."""
    ar = rows['active']
    rr = rows['power']

    f_card_start(self, ar, root)
    my_index = ar.list.index(self)  # The index of this retrigger card

    if my_index == 0:
        print(f'{ar.list.index(self)} {self.name}:\tNo card found to the left!')
    else:
        print(f'{ar.list.index(self)} {self.name}:\tRe-activating card to the left!')
        ar.list[ar.list.index(self) - 1].function(rows, root)  # I don't like passing the active row every time.
    f_card_end(self, ar, root)
card_dict.update({'Re-Trigger': Card(
    name='Re-Trigger', function=f_retrigger_left, image_file='card_images/fp_retrigger.png',
    item_type='prototype', rarity=vars.r_uncommon)})

# TODO: Consider what the point of item types is
#  - Draw pools?
#  - Glorified tags?

token_dict = {}
# Particle Tokens
def f_e_neutrino_token(self, rows, root):
    pr = rows['particle']
    print('oscillating to muon (visually)')
    index = pr.list.index(self)
    print(index)
    self.image_file = 'token_images/fp_token_muon_neutrino.png'
    pass
token_dict.update({'e- Neutrino': Token(
    name='e- Neutrino', function=f_e_neutrino_token, image_file='token_images/fp_token_e_neutrino.png',
    item_type='particle', tags=['electron, neutrino'])})

def f_muon_neutrino_token(self, rows, root):
    print('muon neutrino activated')
    pass
token_dict.update({'Muon Neutrino': Token(
    name='Muon Neutrino', function=f_muon_neutrino_token, image_file='token_images/fp_token_muon_neutrino.png',
    item_type='particle', tags=['muon, neutrino'])})

def f_tau_neutrino_token(self, rows, root):
    print('muon neutrino activated')
    pass
token_dict.update({'Tau Neutrino': Token(
    name='Tau Neutrino', function=f_tau_neutrino_token, image_file='token_images/fp_token_tau_neutrino.png',
    item_type='particle', tags=['tau, neutrino'])})


# Resource Tokens
def f_power_token(self, rows, root):
    ar = rows['active']
    rr = rows['power']

    for card in ar.list[ar.active_index + 1:]:
        if card.power_slots - card.power_tokens > 0:
            card.power_tokens += 1
            self.gui_button.destroy()
            rr.list.pop(rr.list.index(self))
            break
    # f_card_end(self, ar, root)
token_dict.update({'Power': Token(
    name='Power', function=f_power_token, image_file='token_images/fp_token_power.png',
    item_type='resource')})
