import pygame, os
from .ship import Ship

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x,y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0

    def move_lasers(self, vel, enemies):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for enemy in enemies[:]:
                    if laser.collision(enemy):
                        enemies.remove(enemy)
                        self.lasers.remove(laser)
                        self.score += 1
                        break

    def  draw(self, window):
        super().draw(window)
        self.healthbar(window)
        self.scoreboard(window)

    def scoreboard(self, window):
        font = pygame.font.SysFont("Arial", 30)
        score_label = font.render("Score: " + str(self.score), 1, (255, 255, 255))
        window.blit(score_label, (10, 50))

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()
                                             ,10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()* (self.health
                                                                                                        /self.max_health)
                          , 10))