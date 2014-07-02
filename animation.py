import pygame
from images import *
from random import choice

small_explosions = [M_EXPLOSION_1, M_EXPLOSION_2,
                   ]

ANIMATIONS = {"small_explosions": small_explosions,
              "other_things_example": None}

class Animation (pygame.sprite.Sprite):

    container = pygame.sprite.Group()

class Explosion (Animation):

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, Animation.container)

        frameset = choice(ANIMATIONS["small_explosions"])[1:]
        self.image = frameset[0]
        self.frames = frameset[1:]
        self.rect = self.image.get_rect()
        self.frame_count = 0
        self.limiter = 1

    def update (self, time_passed):

        if self.limiter >= 1:
            self.image = self.frames[self.frame_count]
            self.frame_count += 1
            self.limiter = 0
            if self.frame_count > len(self.frames) - 1:
                self.kill()
        else:
            self.limiter += 1

class Warp (Animation):

    def __init__ (self, position):
        pygame.sprite.Sprite.__init__(self, Animation.container)

        self.images = WARP_IMAGE
        self.image = self.images[0]
        self.frame = 1
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update (self, time_passed):

        if self.frame >= 9:
            self.kill()
            del self
        else:
            self.image = self.images[self.frame]
            self.frame += 1

class Sparks (Animation):

    def __init__ (self, position):
        pygame.sprite.Sprite.__init__(self, Animation.container)

        self.images = choice([SPARKS1_IMAGE, SPARKS2_IMAGE])
        self.image = self.images[0]
        self.frame = 1
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1]-5)

    def update (self, time_passed):

        if self.frame >= 16:
            self.kill()
            del self
        else:
            self.image = self.images[self.frame]
            self.frame += 1


class EMP (Animation):

    def __init__ (self, host, duration):
        pygame.sprite.Sprite.__init__(self, Animation.container)

        self.images = WARP_IMAGE
        self.image = self.images[0]
        self.frame = 1
        self.rect = self.image.get_rect()
        self.host = host
        self.duration = [duration[0], duration[1]]
        self.host.disabled = True

    def update (self, time_passed):

        if self.duration[1] >= self.duration[0]:
            self.host.disabled = False
            self.kill()
            self.duration[1] = 0
            del self; return
        else:
            self.duration[1] += 1 * time_passed
        if self.frame >= 9:
            self.frame = 0
        else:
            self.image = self.images[self.frame]
            self.frame += 1
        self.rect.center = self.host.rect.center
        
        
        
