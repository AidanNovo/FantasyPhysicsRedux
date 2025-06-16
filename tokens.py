import tkinter as tk

import common
from common import Item, pretty_print, item_factory


class Token(Item):
    def __init__(self, energy=None, half_life=None, **kwargs):
        super().__init__(**kwargs)
        self.energy = energy  # Particle energy
        self.half_life = half_life  # Particle half-life


# Particle Tokens
# TODO: Make neutrinos actually oscillate randomly.
# TODO: Maybe turn the repeated neutrino oscillation code into a single function for transforming a card in place
def f_e_neutrino_token(self, rows, root):
    from main import initialize_item_image, initialize_item_gui_button, bind_item_instance_function
    pr = rows['particle']

    common.pretty_print(self, pr, 'Oscillating to muon neutrino.')

    index = pr.list.index(self)
    self = item_factory('Muon Neutrino')
    pr.list[index] = self

    # Re-initialize some stuff that would normally get initialized in the create_item function
    initialize_item_gui_button(self, pr)
    initialize_item_image(self)
    bind_item_instance_function(self, pr, index)
common.token_dict.update({'e- Neutrino': Token(
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
common.token_dict.update({'Muon Neutrino': Token(
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
common.token_dict.update({'Tau Neutrino': Token(
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
common.token_dict.update({'Power': Token(
    name='Power', function=f_power_token, image_file='token_images/fp_token_power.png',
    item_type='resource')})