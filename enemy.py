# Enemies
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame
import random
import os
from wall import Wall, SpecialType, SpecialWall

# Stats and image paths
ENEMY_TYPES = {
    'normal': {
        'speed': 1,
        'health': 100,
        'damage': 2,
        'color': (255,0,0),
        'size': 30,
        'image_paths': {
            'left': 'img/normal_enemy_left.png',
            'right': 'img/normal_enemy_right.png',
            'up': 'img/normal_enemy_up.png',
            'down': 'img/normal_enemy_down.png'}
    },
    'fast': {   # Weaker but faster enemy
        'speed': 2,
        'health': 50,
        'damage': 1,
        'color': (0,255,0),
        'size': 30,
        'image_paths': {
            'left': 'img/fast_enemy_left.png',
            'right': 'img/fast_enemy_right.png',
            'up': 'img/fast_enemy_up.png',
            'down': 'img/fast_enemy_down.png'}
    },
    'tank': {   # Stronger but slower enemy
        'speed': 0.5,
        'health': 200,
        'damage': 3,
        'color': (0,0,255),
        'size': 50,
        'image_paths': {
            'left': 'img/tank_enemy_left.png',
            'right': 'img/tank_enemy_right.png',
            'up': 'img/tank_enemy_up.png',
            'down': 'img/tank_enemy_down.png'}
    }
}

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, room_walls, WINDOW_WIDTH, WINDOW_HEIGHT):
        super().__init__()

        # Characteristics
        self.type = enemy_type
        self.stats = ENEMY_TYPES[enemy_type].copy()
        self.health = self.stats['health']

        # Spawn in valid location
        self.spawn_in_room(room_walls, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Movement
        self.change_x = random.choice([-1, 1]) * self.stats['speed']
        self.change_y = random.choice([-1, 1]) * self.stats['speed']

        # Image
        self.images = self.load_directional_images()
        self.current_direction = self.get_initial_direction()
        self.image = self.images[self.current_direction]
        self.rect = self.image.get_rect(x=self.x, y=self.y)

        # Movement
        self.direction_change_timer = 0
        self.direction_change_interval = random.randint(60, 180)

    # Image loading
    def load_directional_images(self):
        images = {}
        for direction, path in self.stats['image_paths'].items():
            try:
                full_path = os.path.join(os.path.dirname(os.path.dirname('CS1_Lab03.01')), path)
                image = pygame.image.load(full_path).convert_alpha()
                images[direction] = pygame.transform.scale(image, (self.stats['size'], self.stats['size']))
            except pygame.error as e:
                print(f"Could not load image: {path}: {e}")
                fallback = pygame.Surface(self.stats['size'], self.stats['size'])
                fallback.fill((255, 255, 255))
                images[direction] = fallback
                return fallback
        return images

    # Get direction for image loading
    def get_initial_direction(self):
        if self.change_x < 0:
            return 'left'
        elif self.change_x > 0:
            return 'right'
        elif self.change_y < 0:
            return 'up'
        else:
            return 'down'

    # Spawn in valid location
    def spawn_in_room(self, room_walls, WINDOW_WIDTH, WINDOW_HEIGHT):
        max_attempts = 100
        for _ in range(max_attempts):
            self.x = random.randint(50, WINDOW_WIDTH - 50)
            self.y = random.randint(50, WINDOW_HEIGHT - 50)

            spawn_rect = pygame.Rect(self.x, self.y, self.stats['size'], self.stats['size'])

            if not any(spawn_rect.colliderect(wall.rect) for wall in room_walls):
                return

        # Fallback to default position
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2


    # Movement and sprite changing
    def move(self, walls):
        self.direction_change_timer += 1
        if self.direction_change_timer >= self.direction_change_interval:
            self.change_direction()

        original_x = self.rect.x
        original_y = self.rect.y

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.change_x < 0:
            self.current_direction = 'left'
            self.image = self.images[self.current_direction]
        elif self.change_x > 0:
            self.current_direction = 'right'
            self.image = self.images[self.current_direction]
        elif self.change_y < 0:
            self.current_direction = 'up'
            self.image = self.images[self.current_direction]
        else:
            self.current_direction = 'down'
            self.image = self.images[self.current_direction]

        # Collisions
        collision = False
        for wall in walls:
            if isinstance(wall, SpecialWall):
                if wall.check_collision(self):
                    collision = True
                    break
            else:
                if self.rect.colliderect(wall.rect):
                    collision = True
                    break

        if collision:
            self.rect.x = original_x
            self.rect.y = original_y
            self.change_direction()

    # Random direction changes
    def change_direction(self):
        self.change_x = random.choice([-1, 0, 1]) * self.stats['speed']
        self.change_y = random.choice([-1, 0, 1]) * self.stats['speed']

        if self.change_x == 0 and self.change_y == 0:
            self.change_x = random.choice([-1, 1]) * self.stats['speed']

        self.direction_change_timer = 0
        self.direction_change_interval = random.randint(60, 180)

    def __repr__(self):
        return f"Enemy(type={self.type}, health={self.health}, pos=({self.rect.x}, {self.rect.y}))"