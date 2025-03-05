import pygame
from wall import Wall, SpecialWall

# Base class for rooms
class Room(object):
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

class Room1(Room):
    def __init__(self):
        super().__init__()

        # Walls in form of [x, y, width, height, color]
        walls = [[]]

        # Create walls and add to list
        for wall in walls:
            wall = Wall(wall[0], wall[1], wall[2], wall[3], wall[4])
            self.wall_list.add(wall)

class Room2(Room):
    def __init__(self):
        super().__init__()

        # Walls
        walls = [[]]

        # Loop
        for wall in walls:
            wall = Wall(wall[0], wall[1], wall[2], wall[3], wall[4])
            self.wall_list.add(wall)

class Room3(Room):
    def __init__(self):
        super().__init__()

        # Walls
        walls = [[]]

        # Loop
        for wall in walls:
            wall = Wall(wall[0], wall[1], wall[2], wall[3], wall[4])
            self.wall_list.add(wall)