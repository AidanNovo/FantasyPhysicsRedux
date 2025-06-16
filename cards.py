import tkinter as tk
from copy import deepcopy
import time

import common


class Item:
    # f stands for function
    def f_default(self):
        """Default function as a fallback."""
        raise Exception('Card/token activated with default function.')

    def __init__(self, name='', image_file=None, function=f_default, prerun_function=None, item_type='', tags=()):
        self.name = name
        self.image_file = image_file
        self.function = function
        self.prerun_function = prerun_function  # A special function that runs before normal card activation starts
        self.item_type = item_type
        self.tags = tags

    def __repr__(self):
        return self.name


class Card(Item):
    """The general class used for each card in the game."""
    def __init__(self, rarity=common.r_common, param=0.0, power_slots=0, power_tokens=0, **kwargs):
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
    def __init__(self, energy=None, half_life=None, **kwargs):
        super().__init__(**kwargs)
        self.energy = energy  # Particle energy
        self.half_life = half_life  # Particle half-life


def pretty_print(self, holder, message):
    """Print the card's activation message with some standardized formatting and spacing."""
    target_length = 20  # The number of characters that will appear to the left of the message
    header_length = len(f'{holder.list.index(self)} {self.name}:')
    delta = target_length - header_length

    if delta > 0:
        spacer = ' ' * delta
    else:
        spacer = ' '

    print(f'{holder.list.index(self)} {self.name}:{spacer}{message}')


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

    if common.do_slow_activation.get():
        wait_for_spacebar()
    else:
        time.sleep(1)

    self.activity_string = '--'
    self.gui_button.configure(text=self.status_string(), compound=tk.TOP)
    root.update()
    pass

# def f_t_test(self, ar, pr, root):
#     print('token activated')

def item_factory(item_name):
    """Return a deepcopy of an item from card_dict/token_dict.

    Args:
        item_name: The desired item's key in card_dict/token_dict.

    Returns:
        A deepcopy of the item associated with the given key.
    """

    global card_dict
    global token_dict

    try:  # Note: This requires that we never have a card and token with the same internal name
        return deepcopy(card_dict[item_name])
    except KeyError:
        return deepcopy(token_dict[item_name])


card_dict = {}  # Huge master dict of all the cards and their effects.

# CARD DEFINITIONS GO BELOW HERE
# Analysis Cards
def f_machine_learning(self, rows, root):
    """Generate score from data based on the card's current multiplier, then increase the multiplier."""
    ar = rows['active']

    f_card_start(self, ar, root)
    if self.power_tokens == 0: # Card requires 1 token to run
        pretty_print(self, ar, 'Unpowered')
    else:
        # Increase score
        score_increase = common.data * self.param
        common.score += score_increase

        for card in ar.list:
            if 'computer' in card.tags:  # Perma-increase multiplier by the number of computer cards in your row
                self.param += 0.1
            self.param = round(self.param, 2)

        pretty_print(self, ar, f'Generated {score_increase} score from {common.data} data! '
                               f'ML multiplier increased to {self.param}.')

    f_card_end(self, ar, root)
card_dict.update({'Machine Learning': Card(
    name='Machine Learning', function=f_machine_learning, image_file='card_images/fp_machine_learning.png',
    item_type='analysis', tags=['computer'], param=0.8, power_slots=1)})


# Detector Cards
def f_icecube(self, rows, root):  # Currently, this is exactly the same as f_super_kamiokande
    """Generate data from neutrino tokens."""
    ar = rows['active']
    pr = rows['particle']

    f_card_start(self, ar, root)
    for particle in pr.list:
        if particle.name == 'e- Neutrino' or particle.name == 'Muon Neutrino' or particle.name == 'Tau Neutrino':
            common.data += 1000
            pretty_print(self, ar, 'Neutrino detected, data increased by 1000!')
        else:
            pass
    f_card_end(self, ar, root)
card_dict.update({'IceCube': Card(
    name='IceCube', function=f_icecube, image_file='card_images/fp_icecube.png',
    item_type='detector', tags=['neutrino', 'astro'])})

def f_super_kamiokande(self, rows, root):
    """Generate data from neutrino tokens."""
    ar = rows['active']
    pr = rows['particle']

    f_card_start(self, ar, root)
    for particle in pr.list:
        if particle.name == 'e- Neutrino'or particle.name == 'Muon Neutrino' or particle.name == 'Tau Neutrino':
            common.data += 1000
            pretty_print(self, ar, 'Neutrino detected, data increased by 1000!')
        else:
            pass
    f_card_end(self, ar, root)
card_dict.update({'Super-Kamiokande': Card(
    name='Super-Kamiokande', function=f_super_kamiokande, image_file='card_images/fp_super_k.png',
    item_type='detector', tags=['neutrino', 'astro'])})


# Physics Cards (temporary name)
def f_neutrino_oscillation(self, rows, root):
    ar = rows['active']

    f_card_start(self, ar, root)
    pretty_print(self, ar, 'Multiplying score for each [neutrino] card...')
    for card in ar.list:
        if 'neutrino' in card.tags:
            common.score = common.score * 1.5
            pretty_print(self, ar, f'Multiplied score by 1.5 due to {ar.list.index(card)} '
                                   f'{card.name}`s [neutrino] tag! Score is now {common.score}!')
    f_card_end(self, ar, root)
card_dict.update({'Neutrino Oscillation': Card(
    name='Neutrino Oscillation', function=f_neutrino_oscillation, image_file='card_images/fp_neutrino_oscillation.png',
    item_type='physics', tags=['neutrino'], rarity=common.r_rare)})

# Special Cards
def f_fission_reactor(self, rows, root):
    ar = rows['active']
    pr = rows['particle']

    from main import create_item
    f_card_start(self, ar, root)
    create_item('e- Neutrino', pr)
    pretty_print(self, ar, 'Created an e- Neutrino token!')

    for _ in range(5):  # Make 5 power tokens
        create_item('Power', common.power_row)

    f_card_end(self, ar, root)
card_dict.update({'Fission Reactor': Card(
    name='Fission Reactor', function=f_fission_reactor, image_file='card_images/fp_fission_reactor.png',
    item_type='special', tags=['reactor', 'neutrino'], rarity=common.r_uncommon)})

def f_lbnf_beam(self, rows, root):
    ar = rows['active']
    pr = rows['particle']

    from main import create_item
    f_card_start(self, ar, root)
    if self.power_tokens == 0: # Card requires at least 1 token to run
        pretty_print(self, ar, 'Unpowered!')
    else:
        for _ in range(self.power_tokens):
            create_item('e- Neutrino', pr)
        pretty_print(self, ar, 'Generated an e- Neutrino.')
    f_card_end(self, ar, root)
card_dict.update({'LBNF Beam': Card(
    name='LBNF Beam', function=f_lbnf_beam, image_file='card_images/fp_lbnf_beam.png',
    item_type='special', tags=['beam', 'neutrino'], power_slots=3)})


# Prototype Cards
def f_neutrino_generator(self, rows, root):
    ar = rows['active']

    from main import create_item
    f_card_start(self, ar, root)
    create_item('e- Neutrino', common.particle_row)
    pretty_print(self, ar, 'Created an e- Neutrino token!')
    f_card_end(self, ar, root)
card_dict.update({'Neutrino Gen': Card(
    name='Neutrino Gen', function=f_neutrino_generator, image_file='card_images/fp_neutrino_gen.png',
    item_type='prototype', tags=['neutrino'], rarity=common.r_uncommon)})

def f_recompute(self, rows, root):
    """Re-activate all cards with the 'computer' tag."""
    ar = rows['active']
    rr = rows['power']

    f_card_start(self, ar, root)
    for card in reversed(ar.list):  # Process in reverse so that retriggers activate left to right (remember, FILO)
        if 'computer' in card.tags:
            pretty_print(self, ar, f'Re-activating {ar.list.index(card)} {card.name} due to its computer tag!')
            common.stack.append(common.StackEvent(card, card.function, (rows, root)))
    f_card_end(self, ar, root)
card_dict.update({'ReCompute': Card(
    name='ReCompute', function=f_recompute, image_file='card_images/fp_recompute.png',
    item_type='prototype', rarity=common.r_uncommon)})

def f_retrigger_left(self, rows, root):
    """Re-activate the ability of the item to the left."""
    ar = rows['active']
    rr = rows['power']  # Power row is rr not pr because particle row needs to be pr

    f_card_start(self, ar, root)
    my_index = ar.list.index(self)  # The index of this retrigger card

    if my_index == 0:
        pretty_print(self, ar, 'No card found to the left!')
    else:
        pretty_print(self, ar, 'Re-activating card to the left!')
        card_left = ar.list[ar.list.index(self) - 1]
        common.stack.append(common.StackEvent(card_left, card_left.function, (rows, root)))

    f_card_end(self, ar, root)
card_dict.update({'Re-Trigger': Card(
    name='Re-Trigger', function=f_retrigger_left, image_file='card_images/fp_retrigger.png',
    item_type='prototype', rarity=common.r_uncommon)})

def f_add_computer_bonus(self, rows, root):
    """Add an interpreter that gives bonus points for every computer card activation."""
    ar = rows['active']
    rr = rows['power']

    f_card_start(self, ar, root)
    pretty_print(self, ar, 'Doing nothing! (Card has no active effect)')
    f_card_end(self, ar, root)
def f_prerun_add_computer_bonus(self, rows, root):
    ar = rows['active']

    def f_computer_bonus_interpreter(event):
        # global common.score
        if 'computer' in event.origin.tags:
            common.score += 100
            print('Score increased by 100! (Activated by computer bonus passive)')

    pretty_print(self, ar, 'Adding passive effect: +100 points on computer card activation.')
    computer_bonus = common.Interpreter(f_computer_bonus_interpreter)
    common.interpreters.append(computer_bonus)
card_dict.update({'Add Computer Bonus': Card(
    name='Add Computer Bonus', function=f_add_computer_bonus, prerun_function=f_prerun_add_computer_bonus,
    image_file='card_images/fp_add_computer_bonus.png',
    item_type='prototype', rarity=common.r_uncommon)})

token_dict = {}
# Particle Tokens
# TODO: Make neutrinos actually oscillate randomly.
# TODO: Maybe turn the repeated neutrino oscillation code into a single function for transforming a card in place
def f_e_neutrino_token(self, rows, root):
    from main import initialize_item_image, initialize_item_gui_button, bind_item_instance_function
    pr = rows['particle']

    pretty_print(self, pr, 'Oscillating to muon neutrino.')

    index = pr.list.index(self)
    self = item_factory('Muon Neutrino')
    pr.list[index] = self

    # Re-initialize some stuff that would normally get initialized in the create_item function
    initialize_item_gui_button(self, pr)
    initialize_item_image(self)
    bind_item_instance_function(self, pr, index)
token_dict.update({'e- Neutrino': Token(
    name='e- Neutrino', function=f_e_neutrino_token, image_file='token_images/fp_token_e_neutrino.png',
    item_type='particle', tags=['electron, neutrino'])})

def f_muon_neutrino_token(self, rows, root):
    from main import initialize_item_image, initialize_item_gui_button, bind_item_instance_function
    pr = rows['particle']

    pretty_print(self, pr, 'Oscillating to tau neutrino.')

    index = pr.list.index(self)
    self = item_factory('Tau Neutrino')
    pr.list[index] = self

    # Re-initialize some stuff that would normally get initialized in the create_item function
    initialize_item_gui_button(self, pr)
    initialize_item_image(self)
    bind_item_instance_function(self, pr, index)
token_dict.update({'Muon Neutrino': Token(
    name='Muon Neutrino', function=f_muon_neutrino_token, image_file='token_images/fp_token_muon_neutrino.png',
    item_type='particle', tags=['muon, neutrino'])})

def f_tau_neutrino_token(self, rows, root):
    from main import initialize_item_image, initialize_item_gui_button, bind_item_instance_function
    pr = rows['particle']

    pretty_print(self, pr, 'Oscillating to electron neutrino.')

    index = pr.list.index(self)
    self = item_factory('e- Neutrino')
    pr.list[index] = self

    # Re-initialize some stuff that would normally get initialized in the create_item function
    initialize_item_gui_button(self, pr)
    initialize_item_image(self)
    bind_item_instance_function(self, pr, index)
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
