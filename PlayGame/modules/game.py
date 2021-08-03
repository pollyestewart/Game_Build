import pygame

from .gameObject import GameObject
from .player import Player
from .enemy import Enemy


class Game:

    def __init__(self):
        self.width = 800
        self.height = 800
        self.pink_colour = (255, 204, 230)

        self.game_window = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.background = GameObject(0, 0, self.width, self.height, 'GamePlay/assets/background.png')
        self.treasure = GameObject(385, 60, 40, 40, 'GamePlay/assets/treasure.png')

        self.level = 1.0

        self.reset_map()

    def reset_map(self):

        self.player = Player(375, 700, 50, 50, 'GamePlay/assets/player.png', 10)  # 10 pixels per update

        speed = 1 + (self.level * 5)

        if self.level >= 4.0:
            self.enemies = [
                Enemy(0, 600, 50, 50, 'GamePlay/assets/enemy.png', speed),
                Enemy(750, 400, 50, 50, 'GamePlay/assets/enemy.png', speed),
                Enemy(0, 200, 50, 50, 'GamePlay/assets/enemy.png', speed)
            ]
        elif self.level >= 2.0:
            self.enemies = [
                Enemy(0, 600, 50, 50, 'GamePlay/assets/enemy.png', speed),
                Enemy(750, 400, 50, 50, 'GamePlay/assets/enemy.png', speed)
            ]
        else:
            self.enemies = [
                Enemy(0, 600, 50, 50, 'GamePlay/assets/enemy.png', speed)
            ]

    def draw_objects(self):
        self.game_window.fill(self.pink_colour)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x, self.treasure.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))

        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))

        pygame.display.update()

    def move_objects(self, player_direction):
        self.player.move(player_direction, self.height)

        for enemy in self.enemies:
            enemy.move(self.width)


    def detect_collision(self, object1, object2):
        if object1.y > (object2.y + object2.height):
            # if object 1 is below object 2
            return False
        elif (object1.y + object1.height) < object2.y:
            # if object 1 is above object 2
            return False

        if object1.x > (object2.x + object2.width):
            # if object 1 is further right than object 2
            return False
        elif (object1.x + object1.width) < object2.x:
            # if object 1 is further left than object 2
            return False

        else:
            return True

    def check_if_collided(self):
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level = 1.0
                return True

        if self.detect_collision(self.player, self.treasure):
            self.level += 0.5
            return True

        return False


    def run_game_loop(self):

        player_direction = 0

        while True:
            # Handle Events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_direction = -1
                    elif event.key == pygame.K_DOWN:
                        player_direction = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = 0

            # Execute Logic
            self.move_objects(player_direction)

            # Update Display

            self.draw_objects()

            if self.check_if_collided():
                self.reset_map()


            self.clock.tick(60)



