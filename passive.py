""" Created on Jan 8, 2013

@author: Justin """

from __future__ import division
import pygame
from pygame.locals import Rect
from random import uniform
from images import *
from sounds import sfx
import spaceship


class Passive (pygame.sprite.Sprite):

    container = pygame.sprite.RenderPlain()


class Background (pygame.sprite.Sprite):

    container = pygame.sprite.RenderPlain()


class ScrollingBackground(Background):

    def __init__(self, image_path):
        pygame.sprite.Sprite.__init__ (self, Background.container)
        """ Constructor for ScrollingBackground """

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 1

    def update (self, time_passed):

        self.rect.top += (self.speed)# * time_passed)
        if self.rect.top >= self.rect.height:
            self.rect.bottom = 0


class Smoke (Passive):  # MOVE TO ANIMATIONS

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, Passive.container)

        self.image = pygame.transform.rotozoom(
                SMOKE_IMAGE,
                uniform(0, 45),
                uniform(.75, 1.75)).convert_alpha()
        self.frame = 1
        self.rect = self.image.get_rect()
        self.speed = 1
        self.current_alpha = 1
        self.fade_timer = [90,0]

    def update (self, time_passed):

        self.fade_timer[1] += 1
        if self.fade_timer[1] >= self.fade_timer[0]:
            self.kill()
            del self
            return
        self.rect.move_ip(0, 2)
        if self.rect.top > 1000: self.kill()


class Fire (Smoke):  # MAKE FADE LIKE SMOKE AND MOVE TO ANIMATIONS

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, Passive.container)

        self.image = pygame.transform.rotozoom(
                FIRE_IMAGE,
                uniform(0, 45),
                uniform(.75, 1.75))
        self.rect = self.image.get_rect()
        self.speed = 1
        self.fade_timer = [90,0]


class Nuke (Passive):

    def __init__ (self, nuker, enemies, boss):
        pygame.sprite.Sprite.__init__ (self, Passive.container)

        self.image = NUKE_IMAGE # TODO: Make this not suck...
        self.rect = self.image.get_rect()
        self.rect.center = nuker.rect.center
        self.growth = 0
        self.nuker = nuker
        self.enemies = enemies
        self.boss = boss

    def update (self, time_passed):

        if self.growth > 150:
            self.kill()
            self.nuker.nuking = False
            for enemy in self.enemies:
                if type(enemy).__name__ == "Guard":
                    self.boss.guard_out -= 1
                enemy.die(sfx.muffled_explosion)
            if self.boss:
                if self.boss.decreaseHealth(self.nuker.nuke_damage):
                    f = spaceship.Fireball(LASER_IMAGE, 1, 1)
                    f.angle = 0
                    f.rect.center =  self.boss.rect.center
        self.image = pygame.transform.scale(self.image,
                                (int(self.rect.width*1.015), int(self.rect.height*1.015)))
        self.growth += 1


class BossShield(Passive):
    
    def __init__(self, host):
        pygame.sprite.Sprite.__init__ (self, Passive.container)
        
        self.host = host
        self.image = BOSS_SHIELD
        self.rect = self.image.get_rect()
        self.rect.center = self.host.rect.center
    
    def update(self, time_passed):
        
        if hasattr(self.host, "invincible"):
            if self.host.invincible:
                self.rect.center = self.host.rect.center
            else:
                self.kill()
                del self


class PowerUpGlow(Passive):
    
    def __init__(self, host):
        pygame.sprite.Sprite.__init__(self, Passive.container)
        
        self.host = host
        self.image = POWERUP_GLOW
        self.rect = self.image.get_rect()
        self.rect.center = self.host.rect.center
        
    def update(self, time_passed):
        
        if self.host.alive():
            self.rect.center = self.host.rect.center
        else:
            self.kill()


class HealthBar (pygame.sprite.Sprite):
    
    container = pygame.sprite.Group()
    
    def __init__ (self, host, screen, player=False):
        pygame.sprite.Sprite.__init__ (self, self.container)
        
        self.host = host
        self.rgb = [0,255,0]
        self.screen = screen
        self.image = pygame.Surface((0,0)) # Placeholder for non-existent image
        self.is_player_healthbar = player
        self.screen_rect = screen.get_rect()
    
    def update (self, time_passed):
        
        health_per = self.host.armor["T"]/self.host.armor["M"]
        if not self.is_player_healthbar:
            self.rect = Rect(self.host.rect.left,
                             self.host.rect.top,
                             self.host.rect.width * health_per,
                             int(self.host.rect.width/10))
            #self.rect.bottom = self.host.rect.top 
            #self.rect.left = self.host.rect.left
        else:
            self.rect = Rect(10, self.screen_rect.bottom-30,
                             100 * health_per, 20)
        self.rgb[1] = int(255 * health_per)
        self.rgb[0] = 255 - self.rgb[1]
        self.screen.lock()
        try:
            pygame.draw.rect(self.screen, self.rgb, (self.rect))
        except TypeError:
            pass
            #self.kill() # Believed to be caused when ship is killed and math 
                        # causes invalid rgb values to be passed to pygame.draw
        self.screen.unlock()

