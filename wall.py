# Walls
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame
from enum import Enum
import math

# Parent class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, causes_damage=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.causes_damage = causes_damage

    def hit(self):
        if self.causes_damage:
                return 'DAMAGE'
        return None


# Special type
class SpecialType(Enum):

    # Slides
    SLIDING_WALL = 'sliding_wall'

    # Rotates
    ROTATING_WALL = 'rotating_wall'

# Special walls
class SpecialWall(Wall):
    def __init__(self, x, y, width, height, special_type, color=(255,255,255), causes_damage=True):
        super().__init__(x, y, width, height, color, causes_damage)
        self.original_image = self.image.copy()
        self.original_image.fill(color)

        # Characteristics
        self.special_type = special_type
        self.rotated_image = self.original_image.copy()

        if special_type == SpecialType.SLIDING_WALL:
            self.direction = 1
            self.min_y = 20
            self.max_y = 80
            self.speed = 2

        if special_type == SpecialType.ROTATING_WALL:
            self.angle = 0
            self.rotation_speed = 2
            self.original_rect = self.rect.copy()

    # For movement
    def update(self):
        if self.special_type == SpecialType.SLIDING_WALL:
            self.rect.y += self.speed * self.direction
            if self.rect.y >= self.max_y:
                self.direction = -1
            elif self.rect.y <= self.min_y:
                self.direction = 1

        if self.special_type == SpecialType.ROTATING_WALL:
            self.angle += self.rotation_speed
            if self.angle >= 360:
                self.angle -= 360
            self.rotated_image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.rotated_image.get_rect(center=self.rect.center)


    # Draw method
    def draw(self, surface):
        if self.special_type == SpecialType.ROTATING_WALL:
            surface.blit(self.rotated_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

    # Check collisions (mostly for rotating wall)
    def check_collision(self, other_rect):
        if self.special_type == SpecialType.ROTATING_WALL:
            wall_mask = pygame.mask.from_surface(self.rotated_image)
            other_mask = pygame.mask.from_surface(other_rect.image)
            offset = (other_rect.rect.x - self.rect.x, other_rect.rect.y - self.rect.y)
            return wall_mask.overlap(other_mask, offset) is not None
        return self.rect.colliderect(other_rect.rect)

