# Player
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame
from wall import Wall, SpecialType, SpecialWall
from soundmanager import SoundManager

class Player(pygame.sprite.Sprite):

    # Speed
    change_x = 0
    change_y = 0

    def __init__(self, x, y, size=20):
        pygame.sprite.Sprite.__init__(self)
        self.size = size

        self.images = {
            'left': self.load_image('img/player_move_left.png', (self.size, self.size)),
            'right': self.load_image('img/player_move_right.png', (self.size, self.size)),
            'up': self.load_image('img/player_move_up.png', (size, self.size)),
            'down': self.load_image('img/player_move_down.png', (size, self.size))
        }
        self.image = self.images['down']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Health
        self.health = 20
        self.invulnerable = False
        self.invulnerable_timer = 0

        self.sound_manager = SoundManager()

    def load_image(self, path, size):
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, size)
        except pygame.error as e:
            print(f"Could not load image: {path}:{e}")
            fallback = pygame.Surface(size, pygame.SRCALPHA)
            fallback.fill((255, 255, 255))
            return fallback

    def change_speed(self, x, y):
        self.change_x += x
        self.change_y += y

        # Update sprite image
        if x < 0:
            self.image = self.images['left']
        elif x > 0:
            self.image = self.images['right']
        elif y < 0:
            self.image = self.images['up']
        else:
            self.image = self.images['down']

    def move(self, walls):
        collision_walls = []

        # X-axis
        self.rect.x += self.change_x
        for wall in walls:
            # Special walls
            if isinstance(wall, SpecialWall):
                if wall.check_collision(self):
                    if self.change_x > 0:
                        self.rect.right = wall.rect.left
                    else:
                        self.rect.left = wall.rect.right
                    collision_walls.append(wall)
            else:
                # Regular walls
                if self.rect.colliderect(wall.rect):
                    if self.change_x > 0:
                        self.rect.right = wall.rect.left
                    else:
                        self.rect.left = wall.rect.right
                    collision_walls.append(wall)

        # Y-axis
        self.rect.y += self.change_y
        for wall in walls:
            # Special walls
            if isinstance(wall, SpecialWall):
                if wall.check_collision(self):
                    if self.change_y > 0:
                        self.rect.bottom = wall.rect.top
                    else:
                        self.rect.top = wall.rect.bottom

                    if wall not in collision_walls:
                        collision_walls.append(wall)
            else:
                # Regular walls
                if self.rect.colliderect(wall.rect):
                    if self.change_y > 0:
                        self.rect.bottom = wall.rect.top
                    else:
                        self.rect.top = wall.rect.bottom

                    if wall not in collision_walls:
                        collision_walls.append(wall)

        return collision_walls

    # Manage health
    def take_damage(self, amount):
        if not self.invulnerable:
            self.health -= amount

            # Prevent multiple hits at once
            self.invulnerable = True
            self.invulnerable_timer = 30

            # Check for death
            if self.health <= 0:
                return True

            return False

    def update(self):
        # Invulnerability timer
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
