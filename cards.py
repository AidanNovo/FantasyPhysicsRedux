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
            card.gui_button.configure(text=f'{card.gui_button["text"]} {"(P)"*tokens_added}')
            print(f'Allocated {tokens_added} power token(s) to {active_row.index(card)} {card}!')

            # card.gui_button.configure(text='(P)'*card.power_tokens, compound=tk.TOP)
        if vars.unused_power_tokens == 0:
            print('All power tokens allocated!')
            break

# f stands for function
def f_default():
    """Default function as a fallback."""
    raise Exception('Card/token activated with undefined function')

def f_card_start(self, ar, root):
    """Perform functions universal to all cards at activation start."""
    self.activity_string = 'ACTIVE'
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

def f_t_test(self):
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


def card_factory(card_name):
    """Factory method."""

    global card_dict

    return deepcopy(card_dict[card_name])


# Huge master dict of all the cards and their effects.
card_dict = {}

# Analysis Cards
def f_machine_learning(self, ar, root):
    """Generate score from data based on the card's current multiplier, then increase the multiplier."""
    f_card_start(self, ar, root)
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
    f_card_end(self, ar, root)
card_dict.update({'Machine Learning': Card(
    name='Machine Learning', function=f_machine_learning, image_file='card_images/fp_machine_learning.png',
    item_type='analysis', tags=['computer'], param=0.8, power_slots=1)})


# Detector Cards
def f_icecube(self, ar, root):
    """Generate data from neutrino flux."""
    f_card_start(self, ar, root)
    vars.data += vars.neutrino_flux
    print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux}!')
    f_card_end(self, ar, root)
card_dict.update({'IceCube': Card(
    name='IceCube', function=f_icecube, image_file='card_images/fp_icecube.png',
    item_type='detector', tags=['neutrino', 'astro'])})

def f_super_kamiokande(self, ar, root):
    """Generate data from neutrino flux, more efficiently if the neutrino oscillation card is in the active row."""
    f_card_start(self, ar, root)
    if 'Neutrino Oscill.' in [card.name for card in ar]:
        vars.data += vars.neutrino_flux * 1.5
        print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux * 1.5}! (More efficient due to '
              f'neutrino oscillation card)')
    else:
        vars.data += vars.neutrino_flux * 0.8
        print(f'{ar.index(self)} {self.name}:\tData increased by {vars.neutrino_flux * 0.8}!')
    f_card_end(self, ar, root)
card_dict.update({'Super-Kamiokande': Card(
    name='Super-Kamiokande', function=f_super_kamiokande, image_file='card_images/fp_super_k.png',
    item_type='detector', tags=['neutrino', 'astro'])})


# Physics Cards (temporary name)
def f_neutrino_oscillation(self, ar, root):
    f_card_start(self, ar, root)
    print(f'{ar.index(self)} {self.name}\t: Multiplying score for each [neutrino] card...')
    for card in ar:
        if 'neutrino' in card.tags:
            vars.score = vars.score * 1.5
            print(f'{ar.index(self)} {self.name}\t: Multiplied score by 1.5 due to {ar.index(card)} {card.name}`s '
                  f'[neutrino] tag! Score is now {vars.score}!')
    f_card_end(self, ar, root)
    # TODO: As mentioned on the card, come up with a cooler name for this
card_dict.update({'Neutrino Oscillation': Card(
    name='Neutrino Oscillation', function=f_neutrino_oscillation, image_file='card_images/fp_neutrino_oscillation.png',
    item_type='physics', tags=['neutrino'], rarity=vars.r_rare)})


# Special Cards
def f_fission_reactor(self, ar, root):
    f_card_start(self, ar, root)
    vars.neutrino_flux += 1000
    print(f'{ar.index(self)} {self.name}\t: Increased Neutrino Flux by 1000 (flux is now {vars.neutrino_flux}).')

    vars.unused_power_tokens += 5
    print(f'{ar.index(self)} {self.name}\t: Added 5 power tokens to the pool! Attempting to allocate power to cards...')

    i = ar.index(self)
    allocate_power_tokens(i, ar)
    f_card_end(self, ar, root)
card_dict.update({'Fission Reactor': Card(
    name='Fission Reactor', function=f_fission_reactor, image_file='card_images/fp_fission_reactor.png',
    item_type='special', tags=['reactor', 'neutrino'], rarity=vars.r_uncommon)})

def f_lbnf_beam(self, ar, root):
    f_card_start(self, ar, root)
    if self.power_tokens == 0: # Card requires at least 1 token to run
        print(f'{ar.index(self)} {self.name}:\tUnpowered!')
    else:
        vars.neutrino_flux += 1000 * self.power_tokens
        print(f'{ar.index(self)} {self.name}\t: Increased Neutrino Flux by {1000 * self.power_tokens} '
              f'(flux is now {vars.neutrino_flux}).')
    f_card_end(self, ar, root)
card_dict.update({'LBNF Beam': Card(
    name='LBNF Beam', function=f_lbnf_beam, image_file='card_images/fp_lbnf_beam.png',
    item_type='special', tags=['beam', 'neutrino'], power_slots=3)})


# Prototype Cards
def f_neutrino_generator(self, ar, root):
    """Increase the current neutrino flux."""
    f_card_start(self, ar, root)
    vars.neutrino_flux += 500
    print(f'{ar.index(self)} {self.name}:\tIncreased Neutrino Flux by 500 (flux is now {vars.neutrino_flux}).')
    f_card_end(self, ar, root)
card_dict.update({'Neutrino Gen': Card(
    name='Neutrino Gen', function=f_neutrino_generator, image_file='card_images/fp_neutrino_gen.png',
    item_type='prototype', tags=['neutrino'], rarity=vars.r_uncommon)})

def f_recompute(self, ar, root):
    """Re-activate all cards with the 'computer' tag."""
    f_card_start(self, ar, root)
    for card in ar:
        if 'computer' in card.tags:
            print(f'{ar.index(self)} {self.name}:\tRe-activating {ar.index(card)} {card.name} due to its computer tag!')
            card.function(ar, root)
    f_card_end(self, ar, root)
card_dict.update({'ReCompute': Card(
    name='ReCompute', function=f_recompute, image_file='card_images/fp_recompute.png',
    item_type='prototype', rarity=vars.r_uncommon)})

def f_retrigger_left(self, ar, root):
    """Re-activate the ability of the card_name to the left."""
    f_card_start(self, ar, root)
    active_row = ar
    my_index = active_row.index(self)  # The index of this retrigger card

    if my_index == 0:
        print(f'{ar.index(self)} {self.name}:\tNo card found to the left!')
    else:
        print(f'{ar.index(self)} {self.name}:\tRe-activating card to the left!')
        active_row[active_row.index(self) - 1].function(active_row, root)  # I don't like passing the active row every time.
    f_card_end(self, ar, root)
card_dict.update({'Re-Trigger': Card(
    name='Re-Trigger', function=f_retrigger_left, image_file='card_images/fp_retrigger.png',
    item_type='prototype', rarity=vars.r_uncommon)})

# TODO: Consider whether particle should be a tag or a token subtype. Perhaps we don't even need the TOKEN supertype?
# TODO: Consider what the point of item types is
#  - Draw pools?
#  - Glorified tags?

token_dict = {
    # Particle Tokens
    # 'e- Neutrino':      Token(name='e- Neutrino', item_type='particle', tags=['electron', 'neutrino'],
    #                           image_file='token_images/fp_token_e_neutrino.png', function=f_t_test),

    # Resource Tokens
    'Power':            Token(name='Power', item_type='resource', tags=['resource'],
                              image_file='token_images/fp_token_power.png', function=f_t_test),
}