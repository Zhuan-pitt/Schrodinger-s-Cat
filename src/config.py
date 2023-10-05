import pygame
import os
from src.sound import Sound
from src.theme import Theme

class Config:

    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav'))
        self.button_sound = Sound(
            os.path.join('assets/sounds/button.wav'))
        self.cat_sound = Sound(
            os.path.join('assets/sounds/meow.wav'))
        self.collapse_sound = Sound(
            os.path.join('assets/sounds/swish.wav'))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        #theme pattern = white, black,last black,last white,move on white,move on black
        yellow = Theme('#FFEB9B','#D2A500','#64F0FF','#00DCF0',"#f03232",'#FAAAAA')
        self.themes = [yellow]