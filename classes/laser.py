import pygame


class Laser:
    def __init__(self, x, y, img, vel=5):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.vel

    def off_screen(self, height):
        return not(self.y < height and self.y > 0)

    def json(self):
        return {"x": self.x, "y": self.y, "vel": self.vel}
