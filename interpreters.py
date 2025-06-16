import tkinter as tk

import common
from common import Item


class Interpreter(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.function = None
        # self.f_args = None

def f_main_interpreter(self, event):
    event.function(*event.f_args)
common.interpreter_dict.update({'Main Interpreter': Interpreter(
    name='Main Interpreter', function=f_main_interpreter, image_file='interpreter_images/fp_interpreter_placeholder.png')})


def f_computer_bonus_interpreter(self, event):
    if 'computer' in event.origin.tags:
        common.score += 100
        print('Score increased by 100! (Activated by computer bonus passive)')
common.interpreter_dict.update({'Computer Bonus Interpreter': Interpreter(
    name='Computer Bonus Interpreter', function=f_computer_bonus_interpreter, image_file='interpreter_images/fp_interpreter_placeholder.png',
)})
