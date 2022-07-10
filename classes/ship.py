class Ship:
    def __init__(self, ship_map, health=100):
        self.x = ship_map["x"]
        self.y = ship_map["y"]
        self.vel_x = ship_map["vel_x"]
        self.vel_y = ship_map["vel_y"]
        self.laser_vel = ship_map["laser_vel"]
        self.recharge_time = ship_map["recharge_time"]
        self.laser_x_offset = ship_map["laser_x_offset"]
        self.laser_y_offset = ship_map["laser_y_offset"]
        self.is_player = ship_map["is_player"]
        self.ship_img = None
        self.laser_img = None
        self.health = health
        self.recharging = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def after_shoot(self, fps):
        self.recharging += self.recharge_time * fps

    def move_horizontal(self, direction, screen_width):
        self.x += self.vel_x * direction
        if self.x < 0:
            self.x = 0
        elif self.x + self.get_width() > screen_width:
            self.x = screen_width - self.get_width()

    def move_vertical(self, direction):
        self.y += self.vel_y * direction

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def is_recharged(self):
        return self.recharging == 0

    def recharge(self):
        if self.recharging > 0:
            self.recharging -= 1

    def json(self):
        return {
            "x": self.x,
            "y": self.y,
            "vel_x": self.vel_x,
            "vel_y": self.vel_y,
            "health": self.health,
            "laser_vel": self.laser_vel
        }
