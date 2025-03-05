import pygame
from wall import Wall

class Player(pygame.sprite.Sprite):

    # Speed
    change_x = 0
    change_y = 0

    def __init__(self, x, y)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def change_speed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


