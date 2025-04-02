# Maze Runner
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame
import random

from highscoremanager import HighscoreManager
from wall import Wall, SpecialType, SpecialWall
from room import Room, Room1, Room2, Room3
from player import Player
from enemy import Enemy, ENEMY_TYPES
from coin import Coin
from soundmanager import SoundManager

# Set up game
def reset_game(WINDOW_WIDTH, WINDOW_HEIGHT):
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    moving_sprites = pygame.sprite.Group()

    # Set player
    player = Player(50, 50)
    player.health = 10
    player.invulnerable = False
    player.invulnerable_timer = 0
    moving_sprites.add(player)
    score = 0

    rooms = []

    room = Room1()
    rooms.append(room)

    room = Room2()
    rooms.append(room)

    room = Room3()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    # Enemies and coins
    for room in rooms:
        room.enemy_sprites = pygame.sprite.Group()
        enemy_types = ['normal', 'fast', 'tank']
        for _ in range(4):
            enemy_type = random.choice(enemy_types)
            enemy = Enemy(enemy_type, room.wall_list, WINDOW_WIDTH, WINDOW_HEIGHT)
            room.enemy_sprites.add(enemy)
            moving_sprites.add(enemy)

        room.coin_sprites = pygame.sprite.Group()
        for _ in range(6):
            coin = Coin(room.wall_list, WINDOW_WIDTH, WINDOW_HEIGHT)
            room.coin_sprites.add(coin)

    return all_sprites, moving_sprites, player, rooms, current_room, current_room_no, score


# High scores
def handle_highscore(screen, score):
    font = pygame.font.SysFont(None, 36)
    highscore_manager = HighscoreManager()
    top_scores = highscore_manager.get_highscores()

    # Check if score qualifies
    if len(top_scores) < 5 or score > (top_scores[-1][1] if top_scores else 0):
        initials = highscore_manager.get_player_initials(screen, font)
        if initials:
            highscore_manager.add_highscore(initials, score)

    highscore_manager.draw_high_scores(screen, font)

    return True

# Draw text
def draw_text(screen, text, font, color, y_offset = 0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Main game code
def main():
    # Initialize
    pygame.init()

    # Set up screen
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Font
    font = pygame.font.Font(None, 74)

    # Set title
    pygame.display.set_caption('Maze Runner')

    # Game setup
    all_sprites, moving_sprites, player, rooms, current_room, current_room_no, score = reset_game(WINDOW_WIDTH, WINDOW_HEIGHT)
    sound_manager = SoundManager()

    # Game states
    PLAYING = 'playing'
    WIN = 'win'
    GAME_OVER = 'game_over'
    HIGHSCORE = 'highscore'
    current_state = PLAYING
    initials_prompted = False

    # Clock
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_state in [GAME_OVER, WIN]:
                        current_state = HIGHSCORE
                        initials_prompted = False
                    elif current_state == HIGHSCORE:
                        all_sprites, moving_sprites, player, rooms, current_room, current_room_no, score = reset_game(WINDOW_WIDTH, WINDOW_HEIGHT)
                        current_state = PLAYING

        # Clear screen
        screen.fill((0,0,0))

        # Game logic
        if current_state == PLAYING:

            player.change_x = 0
            player.change_y = 0

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

            # Update player and special walls
            player.update()
            for wall in current_room.wall_list:
                if isinstance(wall, SpecialWall):
                    wall.update()
            for enemy in current_room.enemy_sprites:
                enemy.move(current_room.wall_list)

            current_room_sprites = pygame.sprite.Group(player)
            current_room_sprites.add(current_room.enemy_sprites)
            current_room_sprites.add(current_room.coin_sprites)

            # Move player and wall collisions
            collision_walls = player.move(current_room.wall_list)
            for wall in collision_walls:
                effect = wall.hit()
                if effect == 'DAMAGE' and not player.invulnerable:
                    player.take_damage(1)
                    sound_manager.play_hit()
                    if player.health <= 0:
                        current_state = GAME_OVER

            # Enemy collisions
            for enemy in current_room.enemy_sprites:
                if player.rect.colliderect(enemy.rect):
                    if not player.invulnerable:
                        player.take_damage(enemy.stats['damage'])
                        sound_manager.play_hit()
                        if player.health <= 0:
                            current_state = GAME_OVER

            # Coin collisions
            for coin in current_room.coin_sprites:
                if player.rect.colliderect(coin.rect):
                    coin.kill()
                    # Scoring
                    score += 1
                    sound_manager.play_collect()
                    if score >= 18:
                        current_state = WIN


            # Moving between rooms
            if player.rect.x < -15:
                if current_room_no == 0:
                    current_room_no = 2
                    current_room = rooms[current_room_no]
                    player.rect.x = 790
                elif current_room_no == 2:
                    current_room_no = 1
                    current_room = rooms[current_room_no]
                    player.rect.x = 790
                else:
                    current_room_no = 0
                    current_room = rooms[current_room_no]
                    player.rect.x = 790

            if player.rect.x > 801:
                if current_room_no == 0:
                    current_room_no = 1
                    current_room = rooms[current_room_no]
                    player.rect.x = 0
                elif current_room_no == 1:
                    current_room_no = 2
                    current_room = rooms[current_room_no]
                    player.rect.x = 0
                else:
                    current_room_no = 0
                    current_room = rooms[current_room_no]
                    player.rect.x = 0

            # Draw sprites
            current_room_sprites.draw(screen)
            for wall in current_room.wall_list:
                if isinstance(wall, SpecialWall):
                    wall.draw(screen)
                else:
                    screen.blit(wall.image, wall.rect)


            # Draw health
            health_text = f"Health: {player.health}"
            health_font = pygame.font.Font(None, 36)
            health_surface = health_font.render(health_text, True, (255, 255, 255))
            screen.blit(health_surface, (30, 30))

            # Draw score
            score_text = f"Score: {score}"
            score_font = pygame.font.Font(None, 36)
            score_surface = score_font.render(score_text, True, (255, 255, 255))
            screen.blit(score_surface, (30, 60))

            # Draw remaining items
            items = 0
            for room in rooms:
                items += len(room.coin_sprites)
            items_text = f"Items: {items}"
            items_font = pygame.font.Font(None, 36)
            items_surface = items_font.render(items_text, True, (255, 255, 255))
            screen.blit(items_surface, (30, 90))


        # Handle game over, win, and displaying high scores
        if current_state == GAME_OVER:
            draw_text(screen, "GAME OVER", font, (255, 255, 255))
            draw_text(screen, "Press SPACE to continue", font, (255, 255, 255), 60)
        elif current_state == WIN:
            draw_text(screen, "YOU WIN!", font, (255, 255, 255))
            draw_text(screen, "Press SPACE to continue", font, (255, 255, 255), 60)
        elif current_state == HIGHSCORE:
            if not initials_prompted:
                initials_prompted = handle_highscore(screen, score)
            else:
                highscore_manager = HighscoreManager()
                font = pygame.font.SysFont(None, 36)
                highscore_manager.draw_high_scores(screen, font)


        # Update display
        pygame.display.flip()

        # Game speed
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()