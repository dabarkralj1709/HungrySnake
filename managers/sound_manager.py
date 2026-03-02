import pygame
import os

class SoundManager:

    def __init__(self, base_path):
        pygame.mixer.init()

        self.eat_sound = pygame.mixer.Sound(
            os.path.join(base_path, "assets", "eat.wav")
        )

        self.game_over_sound = pygame.mixer.Sound(
            os.path.join(base_path, "assets", "game_over.wav")
        )

    def play_eat(self):
        self.eat_sound.play()

    def play_game_over(self):
        self.game_over_sound.play()