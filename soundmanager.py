# Sounds
__author__ = 'Gabriel Whangbo-Olvera'
__version__ = '04.02.2025'

import pygame


class SoundManager:
    def __init__(self):
        self.collect_sound = self.load_sound('sounds/collect.wav')
        self.hit_sound = self.load_sound('sounds/hit.wav')
        self.volume = 0.5
        self.set_volume(self.volume)

    def load_sound(self, path):
        try:
            sound = pygame.mixer.Sound(path)
            return sound
        except pygame.error as e:
            print(f"Couldn't load sound: {e}")
            return None

    def play_hit(self):
        if self.hit_sound:
            self.hit_sound.play()

    def play_collect(self):
        if self.collect_sound:
            self.collect_sound.play()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        if self.hit_sound:
            self.hit_sound.set_volume(self.volume)
        elif self.collect_sound:
            self.collect_sound.set_volume(self.volume)
