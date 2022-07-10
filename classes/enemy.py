import pygame
from classes.ship import Ship


class Enemy(Ship):
    def __init__(
            self, enemy_map, health=100
                ):
        super().__init__(enemy_map, health)
        self.ship_img = enemy_map["main_img"]
        self.explosion_img = enemy_map["explosion_img"]
        self.laser_img = enemy_map["laser_img"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def off_screen(self, height):
        return not(self.y < height)
