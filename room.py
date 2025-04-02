# Rooms
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame
import random
from wall import Wall, SpecialType, SpecialWall
from enemy import Enemy, ENEMY_TYPES

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
PINK = (255, 105, 180)


# Base class for rooms
class Room(object):
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

class Room1(Room): # Pink theme
    def __init__(self):
        super().__init__()

        # Walls
        walls = [
                # Outer walls
                    [0, 0, 20, 250, WHITE, False],
                    [0, 350, 20, 250, WHITE, False],
                    [780, 0, 20, 250, WHITE, False],
                    [780, 350, 20, 250, WHITE, False],
                    [20, 0, 760, 20, WHITE, False],
                    [20, 580, 760, 20, WHITE, False],

                # Interior walls
                    [300, 20, 20, 480, PINK, True],
                    [200, 20, 20, 230, PINK, True],
                    [390, 300, 20, 280, PINK, True],
                    [390, 200, 390, 20, PINK, True],
                    [610, 500, 20, 80, PINK, True],
                    [610, 200, 20, 250, PINK, True],
        ]

        for wall in walls:
            wall = Wall(wall[0], wall[1], wall[2], wall[3], wall[4], wall[5])
            self.wall_list.add(wall)

        # Special walls
        sliding_wall = SpecialWall(500, 100, 20, 500, SpecialType.SLIDING_WALL, PINK,True)
        self.wall_list.add(sliding_wall)
        rotating_wall = SpecialWall(150, 300, 20, 200, SpecialType.ROTATING_WALL, PINK, True)
        self.wall_list.add(rotating_wall)


class Room2(Room): # Blue theme
    def __init__(self):
        super().__init__()

        # Walls
        walls = [
                # Outer walls
                    [0, 0, 20, 250, PURPLE, False],
                    [0, 350, 20, 250, PURPLE, False],
                    [780, 0, 20, 250, PURPLE, False],
                    [780, 350, 20, 250, PURPLE, False],
                    [20, 0, 760, 20, PURPLE, False],
                    [20, 580, 760, 20, PURPLE, False],

                # Interior walls
                    [60, 80, 20, 500, BLUE, True],
                    [140, 20, 20, 520, BLUE, True],
                    [220, 250, 20, 330, BLUE, True],
                    [220, 100, 200, 20, BLUE, True],
                    [320, 120, 20, 300, BLUE, True],
                    [340, 300, 300, 20, BLUE, True],
                    [420, 300, 20, 280, BLUE, True],
                    [480, 20, 20, 230, BLUE, True],
                    [580, 20, 20, 230, BLUE, True],
                    [680, 20, 20, 350, BLUE, True]
        ]

        for wall in walls:
            wall = Wall(wall[0], wall[1], wall[2], wall[3], wall[4], wall[5])
            self.wall_list.add(wall)
        rotating_wall = SpecialWall(580, 360, 20, 200, SpecialType.ROTATING_WALL, BLUE, True)
        self.wall_list.add(rotating_wall)


class Room3(Room): # Green theme
    def __init__(self):
        super().__init__()

        # Walls
        walls = [
                # Outer walls
                    [0, 0, 20, 250, RED, False],
                    [0, 350, 20, 250, RED, False],
                    [780, 0, 20, 250, RED, False],
                    [780, 350, 20, 250, RED, False],
                    [20, 0, 760, 20, RED, False],
                    [20, 580, 760, 20, RED, False],

                # Interior walls
                    [100, 280, 600, 20, GREEN, True]
        ]

        for wall in walls:
            wall = Wall(wall[0], wall[1], wall[2], wall[3], wall[4], wall[5])
            self.wall_list.add(wall)

        # Special walls
        sliding_wall = SpecialWall(100, 100, 20, 500, SpecialType.SLIDING_WALL, GREEN, True)
        self.wall_list.add(sliding_wall)
        sliding_wall = SpecialWall(680, 100, 20, 500, SpecialType.SLIDING_WALL, GREEN, True)
        self.wall_list.add(sliding_wall)

        rotating_wall = SpecialWall(280, 30, 20, 250, SpecialType.ROTATING_WALL, GREEN, True)
        self.wall_list.add(rotating_wall)
        rotating_wall = SpecialWall(280, 320, 20, 250, SpecialType.ROTATING_WALL, GREEN, True)
        self.wall_list.add(rotating_wall)
        rotating_wall = SpecialWall(520, 30, 20, 250, SpecialType.ROTATING_WALL, GREEN, True)
        self.wall_list.add(rotating_wall)
        rotating_wall = SpecialWall(520, 320, 20, 250, SpecialType.ROTATING_WALL, GREEN, True)
        self.wall_list.add(rotating_wall)
