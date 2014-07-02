from __future__ import division
import pygame, math
from random import randint,uniform,choice
from spaceship import Fireball
from animation import Explosion
from sounds import sfx
from animation import Warp
from images import *


class EnemyFireball:

    container = pygame.sprite.Group()


class Enemy (pygame.sprite.Sprite):

    container = pygame.sprite.Group()

    def decreaseHealth (self, dmg):

        if not self.invincible:
            self.armor["T"] -= dmg
        return self.armor["T"]

    def die (self, sound, pause=0):

        if pause:
            pass # TODO: Add a time delay if objects need to wait until they are deleted
        sound.play()
        boom = Explosion()
        boom.rect.center = self.rect.center
        self.rect.center = (9999,9999)
        self.kill()

        del self


class Drone (Enemy):

    def __init__ (self, size, player):
        pygame.sprite.Sprite.__init__ (self, Enemy.container)

        self.image = DRONE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (randint((0+150),(size[0]-150)),
                            randint((0+50),(size[1]-500)))
        self.angle = uniform(0, math.pi*2)
        self.invincible = False
        Warp(self.rect.center)
        self.disabled = False
        self.the_enemy = player

        self.armor = {"T": 1.2, "M": 1.2} # T = Total, M = Max
        self.speed = 225
        self.reload_speed = randint(12, 30)
        self.reload_time = self.reload_speed

    def shoot (self):

        bullet = Fireball(FIREBALL_IMAGE, 325)
        Fireball.container.remove(bullet)
        EnemyFireball.container.add(bullet)
        bullet.angle = math.pi*2
        bullet.rect.midtop = self.rect.midbottom

    def move (self):
        """ Moves self on a vector at self.angle. """

        x = self.the_enemy.rect.center
        y = self.rect.center
        dx = (x[0]-y[0])
        dy = (x[1]-y[1])
        distance_player_self = int(math.sqrt(dx**2 + dy**2))
        chance = randint(1, distance_player_self)
        if chance == 1:
            self.angle = (uniform(0, math.pi*2))
        pos = (math.sin(self.angle) * self.speed/100,
                math.cos(self.angle) * self.speed/100)
        self.rect.move_ip(pos)
        self.bounce()

    def bounce (self):
        """ Bounce self if x or y is out of range of the game window. """

        if self.rect.right > 900:
            self.angle = - self.angle
        elif self.rect.left < -100:
            self.angle = - self.angle
        if self.rect.bottom > 900:
            self.angle = math.pi - self.angle
        elif self.rect.top < -100:
            self.angle = math.pi - self.angle

    def update (self, time_passed):

        if self.disabled: return
        self.move()
        if self.reload_time >= self.reload_speed:
            chance = randint(1,100)
            if chance == 1:
                self.shoot()
                self.reload_time = 0
        else:
            self.reload_time += 1

class Bomber (Enemy):

    def __init__ (self, size, player):
        pygame.sprite.Sprite.__init__ (self, Enemy.container)

        self.image = BOMBER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (randint((0+30),(size[0]-30)), 0)
        self.radias = ((self.rect.width/2 + self.rect.height/2)/2)
        self.direction = 1
        self.speed = 275
        self.destination = (size[0]-self.rect.center[0], size[1]+100)
        diff = (self.destination[0]-self.rect.center[0],
                self.destination[1]-self.rect.center[1])
        self.angle = math.atan2(diff[0], diff[1])
        self.reload_speed = [75, 12, 6] #Interval,delay,shots per burst
        self.reload_time = [0, 12, 0]
        self.armor = {"T": 3, "M": 3} # T = Total, M = Max
        self.disabled = False
        self.the_enemy = player
        self.image = pygame.transform.rotate(
                                        self.image, self.angle*(180/math.pi))
        self.invincible = False
        self.screen_ref = size

    def shoot (self, angle, time_passed):

        bullet = Fireball(FIREBALL_IMAGE, 300)
        bullet.angle = angle
        bullet.pos = ((math.sin(bullet.angle) * bullet.speed) * time_passed,
                      (math.cos(bullet.angle) * bullet.speed) * time_passed)
        Fireball.container.remove(bullet)
        EnemyFireball.container.add(bullet)
        bullet.rect.center = self.rect.center

    def update (self, time_passed):

        if self.disabled: return
        self.rect.move_ip((math.sin(self.angle) * self.speed) * time_passed,
                          (math.cos(self.angle) * self.speed) * time_passed)

        if self.reload_time[0] >= self.reload_speed[0]:
            if self.reload_time[1] >= self.reload_speed[1]:
                x = self.the_enemy.rect.center
                y = self.rect.center
                dx = (x[0]-y[0])
                dy = (x[1]-y[1])
                self.shoot(math.atan2(dx, dy), time_passed) # Shoot directly at player
                self.reload_time[1] = 0 # Reset delay (12/60 of a second)
                self.reload_time[2] += 1 # Tally shot
                if self.reload_time[2] == self.reload_speed[2]:
                    self.reload_time[2] = 0 # 6 shots have been fired - reset
                    self.reload_time[0] = 0 #
            else:
                self.reload_time[1] += 1 # Tick delay between shots
        else:
            self.reload_time[0] += 1 # Tick interval between bursts

        if self.rect.top > self.screen_ref[1]:
            self.kill()
            del self


class Warship (Enemy):

    def __init__ (self, size, player):
        pygame.sprite.Sprite.__init__ (self, Enemy.container)

        self.image = WARSHIP_IMAGE
        self.rect = self.image.get_rect()
        self.rect.midbottom = (randint(30,size[0]-30), 0)
        self.radias = ((self.rect.width/2 + self.rect.height/2)/2)
        self.direction = 1
        self.invincible = False
        self.the_enemy = player
        self.armor = {"T": 10, "M": 10} # T = Total, M = Max
        self.disabled = False
        self.speed = 75
        self.reload_speed = int(60 * 2.5)
        self.reload_time = self.reload_speed
        self.gun_sep = self.rect.height/6

    def shoot (self, direction, time_passed):

        curr_gun = 0
        topleft = self.rect.topleft
        topright = self.rect.topright
        for shot in xrange(6):
            bullet = Fireball(FIREBALL_IMAGE, 325)
            Fireball.container.remove(bullet); EnemyFireball.container.add(bullet)
            if direction == "left":
                bullet.rect.center = (topleft[0], topleft[1]+curr_gun)
                bullet.angle = (math.pi*2) * 0.75
            else:
                bullet.rect.center = (topright[0], topright[1]+curr_gun)
                bullet.angle = (math.pi*2) * 0.25
            curr_gun += self.gun_sep

    def update (self, time_passed):

        if self.disabled: return
        if self.rect.top < 1200:
            self.rect.move_ip(0, self.speed * time_passed)
            if self.reload_time >= self.reload_speed:
                self.shoot("left", time_passed)
                self.shoot("right", time_passed)
                self.reload_time = 0
            else:
                self.reload_time += 1
        else:
            self.kill()
            del self

class Boss (Enemy):

    container = pygame.sprite.Group()

    def __init__ (self, power, level, image="boss.png"):
        pygame.sprite.Sprite.__init__(self, self.container)

        self.image = BOSS_IMAGE
        self.rect  = self.image.get_rect()
        self.direction = 1
        self.radias = int((self.rect.width/2.3) + (self.rect.height/2.3)/2)
        self.shot_sound = sfx.boss_shot
        self.invincible = False

        # Dynamic variables based on power and/or level
        self.power = power
        self.level = level
        self.speed = 100
        self.travelled = 0
        self.max_travel = 200
        self.directions = {}
        self.moving = None
        self.disabled = False

        #armor = int((power**3/(power**2/12))/75)
        armor = int(5+(self.level*2)+(power/5)) + 10
        self.armor = {"T": armor, "M": armor} # T = Total, M = Max

    def shoot (self, shots, time_passed):

        self.shot_sound.play()
        angle = 0
        step = (math.pi*2)/shots
        for i in xrange(shots):
            bullet = Fireball(FIREBALL_IMAGE, 350)
            bullet.angle = angle + (uniform(-.25,.25))
            bullet.pos = ((math.sin(bullet.angle) * bullet.speed) * time_passed,
                          (math.cos(bullet.angle) * bullet.speed) * time_passed)
            Fireball.container.remove(bullet)
            EnemyFireball.container.add(bullet)
            bullet.rect.center = (self.rect.center[0], self.rect.center[1]+40)
            angle += step

    def update (self, time_passed):

        if self.disabled: return

        if self.rect.bottom < 250:
            self.rect.move_ip(0, int(self.speed*time_passed))
        else:
            if self.invincible:
                self.invincible = False
            chance = randint(1, 150-(self.level*3))
            if chance == 7:
                self.shoot(randint(5,(15+self.level)), time_passed)
            if chance < 5 and self.moving == None:
                self.directions.update({"right":     (1, 1),
                                        "left":      (-1, 1),
                                        "backright": (-1, -1),
                                        "backleft":  (1, -1)})
                self.moving = choice(["right", "left"])
            if self.moving:
                self.travelled += self.speed * time_passed
                if self.travelled < self.max_travel:
                    self.rect.move_ip(self.directions[self.moving][0],
                                      self.directions[self.moving][1])
                else:
                    if self.travelled < self.max_travel * 2:
                        self.rect.move_ip(
                                    self.directions["back%s" %(self.moving)][0],
                                    self.directions["back%s" %(self.moving)][1])
                    else:
                        self.travelled = 0
                        self.moving = None


