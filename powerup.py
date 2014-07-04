import pygame
from random import randint
from images import *
from sounds import sfx

class PowerUp (pygame.sprite.Sprite):

    container = pygame.sprite.Group()

class Wrench (PowerUp):

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, PowerUp.container)

        self.image = WRENCH_IMAGE
        self.rect  = self.image.get_rect()
        self.speed = randint(50, 300)

    def effect (self, player):

        if player.armor["T"] < player.armor["M"]:
            if player.armor["T"] + 1 == player.armor["M"]:
                sfx.AI_status.play()
            else:
                sfx.AI_repair.play()
            player.armor["T"] += 1
        else:
            player.wrenches += 1
        player.exp += 5

    def update (self, time_passed):

        if self.rect.top < 1000:
            self.rect.move_ip(0, (self.speed * time_passed))
        else:
            self.kill()

class Bullet (PowerUp):

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, PowerUp.container)

        self.image = BULLET_IMAGE
        self.rect  = self.image.get_rect()
        self.speed = randint(50, 300)

    def effect (self, player):

        sfx.power_up.play()
        rs = player.bonus["reload_speed"]
        if rs["steps"][1] < rs["steps"][0]:
            rs["steps"][1] += 1
            rs["duration"][1] = rs["duration"][0]
        else:
            rs["duration"][1] = rs["duration"][0]
        player.exp += 5

    def update (self, time_passed):

        if self.rect.top < 1000:
            self.rect.move_ip(0, (self.speed * time_passed))
        else:
            self.kill()

class MissileReload (PowerUp):

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, PowerUp.container)

        self.image = MISSILE_IMAGE[0]
        self.rect  = self.image.get_rect()
        self.speed = randint(50, 300)

    def effect (self, player):

        sfx.AI_missile.play()
        player.missiles += 1
        player.exp += 5

    def update (self, time_passed):

        if self.rect.top < 1000:
            self.rect.move_ip(0, (self.speed * time_passed))
        else:
            self.kill()



