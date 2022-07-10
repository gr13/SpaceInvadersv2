import os
import pygame
import random
from classes.enemy import Enemy
from classes.player import Player
from classes.laser import Laser


class Game:
    run = True
    FPS = 60

    level = 0
    lives = 5
    score = 0
    lost = False

    enemies = []
    lasers = []

    wave_length = 5
    enemy_vel_x = 0
    enemy_vel_y = 1
    player_vel = 5
    laser_vel = 5

    clock = pygame.time.Clock()
    window = None
    BG = None

    def __init__(self, window, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.window = window
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 60)
        self.load_images()

        self.player = Player(self.PLAYER_MAP)

    def load_images(self):
        # Backgroung
        self.BG = pygame.transform.scale(
            pygame.image.load(os.path.join("assets/imgs", "background-black.png")),
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        # player ship img
        self.PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("assets/imgs", "playership.gif"))
        self.PLAYER_SPACE_SHIP_EXPLOSION = pygame.image.load(
            os.path.join("assets/imgs", "explosion.gif")
        )

        # Lasers
        self.YELLOW_LASER = pygame.image.load(os.path.join("assets/imgs", "pixel_laser_yellow.png"))
        self.YELLOW_LASER = pygame.transform.scale(
            self.YELLOW_LASER,
            (self.YELLOW_LASER.get_width()/2, self.YELLOW_LASER.get_height()/2)
        )

        # enemies
        self.UFO = pygame.image.load(os.path.join("assets/imgs", "ufo.gif"))
        self.FAST_INVIDER = pygame.image.load(os.path.join("assets/imgs", "fastinvader.gif"))
        self.INVIDER_KILLED = pygame.image.load(
            os.path.join("assets/imgs", "invaderkilled.gif")
        )

        self.SAUCER1A = pygame.image.load(os.path.join("assets/imgs", "saucer1a.ico"))
        self.SAUCER1B = pygame.image.load(os.path.join("assets/imgs", "saucer1b.ico"))

        self.SAUCER2A = pygame.image.load(os.path.join("assets/imgs", "saucer2a.ico"))
        self.SAUCER2B = pygame.image.load(os.path.join("assets/imgs", "saucer2b.ico"))

        self.SAUCER3A = pygame.image.load(os.path.join("assets/imgs", "saucer3a.ico"))
        self.SAUCER3B = pygame.image.load(os.path.join("assets/imgs", "saucer3b.ico"))

        self.GREEN_LASER = pygame.image.load(os.path.join("assets/imgs", "pixel_laser_green.png"))
        self.GREEN_LASER = pygame.transform.scale(
            self.GREEN_LASER,
            (self.GREEN_LASER.get_width()/2, self.GREEN_LASER.get_height()/2)
        )
        self.RED_LASER = pygame.image.load(os.path.join("assets/imgs", "pixel_laser_red.png"))
        self.RED_LASER = pygame.transform.scale(
            self.RED_LASER,
            (self.RED_LASER.get_width()/2, self.RED_LASER.get_height()/2)
        )
        self.BLUE_LASER = pygame.image.load(os.path.join("assets/imgs", "pixel_laser_blue.png"))
        self.BLUE_LASER = pygame.transform.scale(
            self.BLUE_LASER,
            (self.BLUE_LASER.get_width()/2, self.BLUE_LASER.get_height()/2)
        )

        self.PLAYER_MAP = {
            "x": 300,
            "y": 630,
            "vel_x": self.player_vel,
            "vel_y": self.player_vel,
            "main_img": self.PLAYER_SPACE_SHIP,
            "explosion_img": self.PLAYER_SPACE_SHIP_EXPLOSION,
            "laser_img": self.YELLOW_LASER,
            "laser_vel": - self.laser_vel,
            "recharge_time": .5,  # recharge, s
            "laser_x_offset": 5,
            "laser_y_offset": - self.PLAYER_SPACE_SHIP.get_height(),
            "is_player": True
        }

        self.ENEMY_COLOR_MAP = {
            "ufo": {
                "main_img": self.UFO,
                "explosion_img": self.INVIDER_KILLED,
                "laser_img": self.GREEN_LASER,
                "vel_x": self.enemy_vel_x,
                "vel_y": self.enemy_vel_y,
                "laser_vel": self.laser_vel,
                "recharge_time": 3,  # recharge, s
                "laser_x_offset": 0,
                "laser_y_offset": self.INVIDER_KILLED.get_height()/2,
                "is_player": False
            },
            "fastinvader": {
                "main_img": self.FAST_INVIDER,
                "explosion_img": self.INVIDER_KILLED,
                "laser_img": self.RED_LASER,
                "vel_x": self.enemy_vel_x,
                "vel_y": self.enemy_vel_y * 2,
                "laser_vel": self.laser_vel,
                "recharge_time": 3,  # recharge, s
                "laser_x_offset": 0,
                "laser_y_offset": self.FAST_INVIDER.get_height()/2,
                "is_player": False
            },
            "saucer1": {
                "main_img": self.SAUCER1A,
                "explosion_img": self.INVIDER_KILLED,
                "laser_img": self.BLUE_LASER,
                "vel_x": self.enemy_vel_x,
                "vel_y": self.enemy_vel_y,
                "laser_vel": self.laser_vel,
                "recharge_time": 3,  # recharge, s
                "laser_x_offset": 0,
                "laser_y_offset": self.SAUCER1A.get_height()/2,
                "is_player": False
            },
            "saucer2": {
                "main_img": self.SAUCER2A,
                "explosion_img": self.INVIDER_KILLED,
                "laser_img": self.BLUE_LASER,
                "vel_x": self.enemy_vel_x,
                "vel_y": self.enemy_vel_y,
                "laser_vel": self.laser_vel,
                "recharge_time": 3,  # recharge, s
                "laser_x_offset": 0,
                "laser_y_offset": self.SAUCER2A.get_height()/2,
                "is_player": False
            },
            "saucer3": {
                "main_img": self.SAUCER3A,
                "explosion_img": self.INVIDER_KILLED,
                "laser_img": self.BLUE_LASER,
                "vel_x": self.enemy_vel_x,
                "vel_y": self.enemy_vel_y,
                "laser_vel": self.laser_vel,
                "recharge_time": 3,  # recharge, s
                "laser_x_offset": 0,
                "laser_y_offset": self.SAUCER3A.get_height()/2,
                "is_player": False
            },
        }

    def collide(self, obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

    def shoot(self, obj):
        if obj.is_recharged() and obj.y > 0:
            laser = Laser(
                obj.x + obj.laser_x_offset,
                obj.y + obj.laser_y_offset,
                obj.laser_img,
                obj.laser_vel
            )
            self.lasers.append(laser)
            obj.after_shoot(self.FPS)
            if not(self.lost) and obj.is_player:
                self.score -= 0.5

    def healthbar(self):
        pygame.draw.rect(
            self.window,
            (255, 0, 0),
            (
                self.SCREEN_WIDTH - 180,
                100,
                150,
                10,
            )
        )

        pygame.draw.rect(
            self.window,
            (0, 255, 0),
            (
                self.SCREEN_WIDTH - 180,
                100,
                150 * (self.player.health / self.player.max_health),
                10,
            )
        )

    def redraw_window(self):
        self.window.blit(self.BG, (0, 0))

        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level: {self.level}", 1, (255, 255, 255))
        score_label = self.main_font.render(f"Score: {self.score}", 1, (255, 255, 255))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (self.SCREEN_WIDTH - level_label.get_width() - 10, 10))
        self.window.blit(score_label, (10, 10 + lives_label.get_height() + 5))

        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        for laser in self.lasers:
            laser.draw(self.window)

        self.healthbar()

        if self.lost:
            lost_label = self.lost_font.render("You lost!", 1, (255, 255, 255))
            self.window.blit(
                lost_label,
                (
                    self.SCREEN_WIDTH/2 - lost_label.get_width()/2, 
                    self.SCREEN_HEIGHT/2 - lost_label.get_height()/2
                )
            )

        # flip & tick
        pygame.display.flip()

    def recharge_objects(self):
        self.player.recharge()
        for enemy in self.enemies:
            enemy.recharge()

    def move_objects(self):
        for laser in self.lasers[:]:
            laser.move()
            if laser.off_screen(self.SCREEN_HEIGHT):
                self.lasers.remove(laser)

        for enemy in self.enemies[:]:
            enemy.move_vertical(1)
            if enemy.off_screen(self.SCREEN_HEIGHT):
                if not(self.lost):
                    self.lives -= 1
                self.enemies.remove(enemy)

            elif self.collide(enemy, self.player):
                self.player.collision()
                if not(self.lost):
                    self.score += 1
                if self.player.is_loose_live():
                    self.lives -= 1
                    if self.lives > 0:
                        self.player.reset_health()
                self.enemies.remove(enemy)

            for laser in self.lasers[:]:
                if self.collide(enemy, laser):
                    if not(self.lost):
                        self.score += 1
                    self.enemies.remove(enemy)
                    self.lasers.remove(laser)

        for enemy in self.enemies:
            if random.randrange(0, 2*self.FPS):
                self.shoot(enemy)

        for laser in self.lasers[:]:
            if self.collide(self.player, laser):
                if not(self.lost):
                    self.player.laser_damage()
                self.lasers.remove(laser)

        if self.lives <= 0:
            self.lost = True

    def main(self):
        while self.run:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return

            self.recharge_objects()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_horizontal(-1, self.SCREEN_WIDTH)
            if keys[pygame.K_RIGHT]:
                self.player.move_horizontal(1, self.SCREEN_WIDTH)
            if keys[pygame.K_UP]:
                self.player.move_vertical(-1, self.SCREEN_HEIGHT)
            if keys[pygame.K_DOWN]:
                self.player.move_vertical(1, self.SCREEN_HEIGHT)
            if keys[pygame.K_SPACE]:  # shoot
                self.shoot(self.player)

            if len(self.enemies) == 0:
                self.level += 1
                for i in range(self.wave_length + self.level):
                    enemy_type = random.choice(
                        ["ufo", "fastinvader", "saucer1",  "saucer2",  "saucer3"]
                    )
                    enemy_map = self.ENEMY_COLOR_MAP[enemy_type]
                    enemy_map["x"] = random.randrange(50, self.SCREEN_WIDTH - 100)
                    enemy_map["y"] = random.randrange(-500, -50)
                    enemy = Enemy(enemy_map)
                    self.enemies.append(enemy)

            self.move_objects()
            self.redraw_window()
