import pygame
from modules.game import Game

if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.run_game_loop()

    pygame.quit()
    quit()