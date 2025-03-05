# Maze Runner
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '03.05.2025'

import pygame
from wall import Wall, SpecialWall
from room import Room, Room1, Room2, Room3
from player import Player

def reset_game(WINDOW_WIDTH, WINDOW_HEIGHT):
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    moving_sprites = pygame.sprite.Group()

    # Set player
    player = Player(50, 50)
    moving_sprites.add(player)

    rooms = []

    room = Room1
    rooms.append(room)

    room = Room2
    rooms.append(room)

    room = Room3
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    return all_sprites, moving_sprites, player, rooms, current_room_no


def main():

    # Set up screen
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Set title
    pygame.display.set_caption('Maze Runner')

    # Game setup
    all_sprites, moving_sprites, player, rooms, current_room_no = reset_game(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Game states
    PLAYING = 'playing'
    WIN = 'win'
    GAME_OVER = 'game_over'
    current_state = PLAYING

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state in [GAME_OVER, WIN]:
                        all_sprites, moving_sprites, player, rooms, current_room_no = reset_game(WINDOW_WIDTH, WINDOW_HEIGHT)
                        current_state = PLAYING

            if current_state == PLAYING:
                # Keyboard movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player.change_speed(-5, 0)
                if keys[pygame.K_RIGHT]:
                    player.change_speed(5, 0)
                if keys[pygame.K_UP]:
                    player.change_speed(0, -5)
                if keys[pygame.K_DOWN]:
                    player.change_speed(0, 5)

                # Clamp
                player.rect.clamp_ip(screen.get_rect())


if __name__ == '__main__':
    main()