import pygame
from classes.ship import Ship


class Player(Ship):
    def __init__(self, player_map, health=100):
        super().__init__(player_map, health)

        self.ship_img = player_map["main_img"]
        self.laser_img = player_map["laser_img"]
        self.explosion_img = player_map["explosion_img"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self, window):
        return super().draw(window)

    def move_vertical(self, direction, screen_hight):
        super().move_vertical(direction)
        if self.y < 0:
            self.y = 0
        elif self.y + self.get_height() > screen_hight:
            self.y = screen_hight - self.get_height()

    def collision(self):
        self.health -= 10

    def is_loose_live(self):
        return self.health <= 0

    def reset_health(self):
        self.health = self.max_health

    def laser_damage(self):
        self.health -= 10
