import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Таймер
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
        }


        # Инструменты
        self.tools = ['axe', 'hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Посевы
        self.seeds = ['tomato', 'corn']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def use_tool(self):
        pass

    def use_seed(self):
        pass

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, time):
        self.frame_index += 4 * time
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active:

            # Передвижение
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Инструменты
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0                        # Каждый раз новая анимка с пробела

            # Смена инструмента
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                if self.tool_index > len(self.tools) - 1:
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

            # Посажено
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # Смена посевов
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                if self.seed_index > len(self.seeds) - 1:
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]
    def get_status(self):
        # Бро афк стоит
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # Использование инструментов
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

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
        self.get_status()
        self.update_timers()

        self.move(time)
        self.animate(time)

