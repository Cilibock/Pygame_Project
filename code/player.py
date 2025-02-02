import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, time):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # горизонтальное движение
        self.pos.x += self.direction.x * self.speed * time
        self.rect.centerx = self.pos.x

        # вертикальное движение
        self.pos.y += self.direction.y * self.speed * time
        self.rect.centery = self.pos.y

    def update(self, time):
        self.input()
        self.move(time)
