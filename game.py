# game.py
import pygame
from settings import *
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cyberpunk RPG Game")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()

    def quit(self):
        pygame.quit()