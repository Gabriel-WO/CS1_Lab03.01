# Coin collectibles
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame
import random
from wall import Wall, SpecialType, SpecialWall

# Coin class (collectible)
class Coin(pygame.sprite.Sprite):
    def __init__(self, room_walls, WINDOW_WIDTH, WINDOW_HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.size = 8
        self.color = (218,165,32) # Gold

        # Circle
        self.spawn_in_room(room_walls, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size,self.size), self.size)
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    # Spawn in valid location
    def spawn_in_room(self, room_walls, WINDOW_WIDTH, WINDOW_HEIGHT):
        max_attempts = 100
        for i in range(max_attempts):
            self.x = random.randint(50, WINDOW_WIDTH - 50)
            self.y = random.randint(50, WINDOW_HEIGHT - 50)
            spawn_rect = pygame.Rect(self.x, self.y, self.size * 2, self.size * 2)
            if not any(spawn_rect.colliderect(wall.rect) for wall in room_walls):
                return
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2




