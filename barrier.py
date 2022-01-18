import pygame
class Barrier:

    def __init__(self):
        self.item_kinds = "images/barrier.png"
        self.speedup = 0.2

    def item_do(self,ai_game):
        ai_game.settings.barrier_flag = True
        ai_game.ship.image = pygame.image.load('images/b_ship.png')