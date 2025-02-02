import pygame
from player import Player
from settings import *
from overlay import Overlay

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

    def run(self, time):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(time)

        self.overlay.display()