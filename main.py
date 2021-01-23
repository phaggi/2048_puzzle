import pygame, sys, random
from pygame.color import THECOLORS


class Game:
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (200, 150, 100, 50))


class StartMenu:
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (200, 150, 100, 50))


class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.scene = 0
        self.button_clicked = False
        self.game = Game()
        self.startMenu = StartMenu()

    def update(self):
        if self.scene == 0:
            self.startMenu.draw(self.screen)
        if self.scene == 1:
            self.game.draw(self.screen)

    def process(self):
        if self.button_clicked:
            self.scene = 1


pygame.init()
screen = pygame.display.set_mode([640, 480])
screen.fill([255, 255, 255])

manager = GameManager(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                manager.button_clicked = True

    manager.update()
    manager.process()
    pygame.display.flip()

pygame.quit()
