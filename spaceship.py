""" Created on Jan 7, 2013

@author: Justin """
from __future__ import division
import pygame
import math
from random import choice
from passive import Smoke,Fire,Nuke
from sounds import sfx
from animation import Explosion,Sparks,EMP
from images import *

class SpaceShip(pygame.sprite.Sprite):
    """   """
    container = pygame.sprite.Group()

    def __init__ (self, screensize):

        pygame.sprite.Sprite.__init__ (self, self.container)
        """ Constructor for SpaceShip."""

        self.moving = set()
        self.shooting = False

        self.opaque = SHIP_IMAGE
        self.transparent = SHIP_IMAGE_TP
        self.image = self.opaque
        self.rect = self.image.get_rect()
        self.radias = ((self.rect.width/2 + self.rect.height/2)/2)
        self.rect.midbottom = (screensize[0]/2,screensize[1]-5)
        self.spawn_point = self.rect.midbottom
        self.screen_ref = screensize

        # Adjustable stats
        self.exp = 0
        self.level = 1
        self.lives = 2
        self.speed = 250
        self.reload_speed = 17.0
        self.armor = {"T": 3, "M": 3} # T = Total, M = Max
        self.guns = 1
        self.bonus = {"reload_speed": {
                        "steps": [2,0], "boost": 4, "duration": [60*15, 0]},
                      }
        self.ranks = {"remaining": 0,
                      "hammer": 0,
                      "sabre": 0,
                      "scorpion": 0,
                      "forge": 0,
                      }
        self.damage = 1
        self.damage_res = 1 # Percent of damage taken. 0.5 == 50%, 1 == 100%
        self.shots_hit = [0.0, 0.0]
        self.reload_time = self.reload_speed
        self.laser_speed = 550
        self.points_until_nuke = 1000
        self.points_until_life = 1500
        self.nukes = 2
        self.nuke_damage = 100
        self.nuking = False # If true, player is invincible
        self.missiles = 3
        #self.missile = True # TODO: Missile construction installation same format as EMP
        self.missile_speed = 350
        self.missile_damage = 10
        self.missile_timer = [60, 60]
        self.emp = None
        self.overloader = None
        self.wrenches = 2

        # Death stuff
        self.respawn_time = 60 * 3  # 60 * seconds
        self.time_until_respawn = 0
        self.is_dead = False
        self.respawned = True


    def decreaseHealth (self, dmg, collision=False):

        if not self.nuking:
            if self.is_dead: return
            self.armor["T"] -= dmg * self.damage_res
            return self.armor["T"]

    def shoot (self):

        if self.is_dead: return
        if self.guns == 1 or self.guns == 3:
            bullet = Fireball(LASER_IMAGE, self.laser_speed, self.damage, player=self)
            bullet.angle = math.pi # Straight up... dawg!
            bullet.rect.center = self.rect.midtop
            sfx.blastershot.play()
            self.shots_hit[0] += 1
        elif self.guns == 2:
            bullet = Fireball(LASER_IMAGE, self.laser_speed, self.damage, player=self)
            bullet.angle = math.pi # Straight up... dawg!
            bullet.rect.center = (self.rect.left, self.rect.top+10)
            bullet = Fireball(LASER_IMAGE, self.laser_speed, self.damage, player=self)
            bullet.angle = math.pi # Straight up... dawg!
            bullet.rect.center = (self.rect.right, self.rect.top+10)
            sfx.blastershot.play()
            self.shots_hit[0] += 2
        if self.guns == 3:
            bullet = Fireball(LASER_IMAGE, self.laser_speed, self.damage, player=self)
            bullet.angle = math.pi # Straight up... dawg!
            bullet.rect.center = (self.rect.left, self.rect.top+10)
            bullet = Fireball(LASER_IMAGE, self.laser_speed, self.damage, player=self)
            bullet.angle = math.pi # Straight up... dawg!
            bullet.rect.center = (self.rect.right, self.rect.top+10)
            sfx.blastershot.play()
            self.shots_hit[0] += 1

    def reviveCheck (self):

        if self.is_dead:
            self.time_until_respawn += 1
            if self.time_until_respawn >= self.respawn_time/2:
                if not self.respawned:
                    self.image = self.transparent
                    self.rect.midbottom = self.spawn_point
                    self.respawned = True
            if self.time_until_respawn >= self.respawn_time:
                self.revive()

    def damageCheck (self, display=False):

        health_per = int(self.armor["T"]/self.armor["M"] * 100)
        if not display:
            if health_per < 67:
                smoke = Smoke()
                smoke.rect.midtop = self.rect.midbottom
                smoke.rect.move_ip (0,-10)
            if health_per < 35:
                fire = Fire()
                fire.rect.midtop = self.rect.midbottom
                fire.rect.move_ip (0,-10)
        else:
            return health_per

    def shotCheck (self):

        rs = self.bonus["reload_speed"]
        boost = rs["steps"][1] * rs["boost"]
        reload_speed = self.reload_speed - boost
        if self.reload_time < reload_speed:
            self.reload_time +=1
        if self.shooting and self.reload_time >= reload_speed:
            self.shoot()
            self.reload_time = 0
        if rs["steps"][1] > 0:
            if rs["duration"][1] > 0:
                rs["duration"][1] -= 1
            else:
                rs["steps"][1] = 0

    def construction (self, time_passed):

        if self.missile_timer[1] <= 0:
            self.missiles += 1
            self.missile_timer[1] = self.missile_timer[0]
        else:
            self.missile_timer[1] -= 1 * time_passed
        if self.exp > self.points_until_nuke:
            sfx.AI_nuke.play()
            self.nukes += 1
            self.points_until_nuke += 1000
        if self.exp > self.points_until_life:
            self.lives += 1
            self.points_until_life += 1500
        # EMP Reload
        try:
            self.emp["timer"][1] -= 1 * time_passed
            if self.emp["timer"][1] <= 0:
                self.emp["timer"][1] = 0
        except TypeError:
            pass

    def getHitPercentage(self):
        
        string = "Accuracy: %s%%"
        if self.shots_hit[1]:
            percent = self.shots_hit[1] / self.shots_hit[0]
            return string % round(percent * 100, 2)
        else:
            return string % 0.0

    def update (self, time_passed):

        tp = time_passed
        if self.moving:
            if "forward" in self.moving and (self.rect.top > 0):
                self.rect.move_ip(0, -self.speed*tp)
            if "back" in self.moving and (self.rect.bottom < self.screen_ref[1]):
                self.rect.move_ip(0, self.speed*tp)
            if "left" in self.moving and (self.rect.left > 0):
                self.rect.move_ip(-self.speed*tp, 0)
            if "right" in self.moving and (self.rect.right < self.screen_ref[0]):
                self.rect.move_ip(self.speed*tp, 0)
        self.shotCheck()
        self.damageCheck()
        self.construction(time_passed)
        self.reviveCheck()

    def missile (self, enemies, boss):

        if self.missiles <= 0: return
        drones   = [sprite for sprite in enemies if type(sprite).__name__ == "Drone"]
        bombers  = [sprite for sprite in enemies if type(sprite).__name__ == "Bomber"]
        warships = [sprite for sprite in enemies if type(sprite).__name__ == "Warship"]
        boss     = boss
        if boss:
            target = boss
        elif warships:
            target = choice(warships)
        elif bombers:
            target = choice(bombers)
        elif drones:
            target = choice(drones)
        else:
            target = None
        missile = Missile(target, self.missile_speed, self.missile_damage)
        missile.optional_targets = (boss, warships, bombers, drones)
        missile.rect.center = self.rect.center
        self.missiles -= 1

    def triggerEmp (self, screen, enemies, boss):
        
        if self.emp and self.emp["timer"][1] == 0:
            if boss:
                EMP(boss, self.emp["duration"])
            for enemy in enemies:
                EMP(enemy, self.emp["duration"])
            self.emp["timer"][1] = self.emp["timer"][0]

    def nuke (self, screen, enemies, boss):

        if self.nukes > 0:
            self.nukes -= 1
            self.nuking = True
            sfx.epic_nuke.play()
            Nuke(self, enemies, boss)

    def repair (self):

        if self.wrenches > 0 and self.armor["T"] < self.armor["M"]:
            self.armor["T"] += 1
            self.wrenches -= 1
            sfx.AI_repair.play()
            sfx.repair.play()
        if self.armor["T"] > self.armor["M"]:
            self.armor["T"] = self.armor["M"]
            sfx.AI_status.play

    def revive (self):

        if self.lives <= 0: return
        self.lives -= 1
        self.is_dead = False
        self.time_until_respawn = 0
        self.image = self.opaque

    def die (self):

        self.is_dead = True
        self.respawned = False
        sfx.muffled_explosion.play()
        boom = Explosion()
        boom.rect.center = self.rect.center
        self.armor["T"] = self.armor["M"]
        self.missiles = 0
        self.wrenches = 0
        if self.lives == 0:
            self.lives = -1
        else:
            self.rect.top = 2160

class Missile (pygame.sprite.Sprite):

    container = pygame.sprite.Group()

    def __init__ (self, target, speed, damage):
        pygame.sprite.Sprite.__init__(self, Fireball.container)

        self.images = MISSILE_IMAGE
        self.orig_image = self.images[1]
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.damage = damage
        self.target = target
        self.optional_targets = None
        self.angle = math.pi*2
        self.ignite_time = [30.0, 0]
        self.ignited = False
        self.drag = 1.0/self.ignite_time[0]

    def explode (self):

        boom = Explosion()
        boom.rect.center = self.rect.center
        self.kill()
        del self

    def newTarget (self):

        self.target = None
        if self.optional_targets[0]:
            self.target = self.optional_targets[0]
            return
        for targets in self.optional_targets[1:]:
            if targets and self.target == None:
                self.target = choice(targets)
            else:
                return


    def update (self, time_passed):

        if not self.ignited:
            drag = self.drag * self.ignite_time[1]
            if self.ignite_time[1] <= 30:
                self.rect.move_ip(0, (self.speed * (1-drag) * time_passed))
                self.ignite_time[1] += 1
            else:
                self.image = self.images[0]
                self.ignited = True
                sfx.missile_launch.play()
        elif self.target:
            x = self.target.rect.center
            if x == (9999,9999):
                self.newTarget()
            y = self.rect.center
            diff = (x[0]-y[0], x[1]-y[1])
            self.angle = math.atan2(diff[0], diff[1])
            self.pos = (math.sin(self.angle) * self.speed * time_passed,
                        math.cos(self.angle) * self.speed * time_passed)
            self.rect.move_ip(self.pos)
            self.image = pygame.transform.rotate(
                    self.orig_image, self.angle*(180/math.pi) - 180)

            smoke = Smoke()
            smoke.rect.center = self.rect.center
            smoke.rect.move_ip (0,-10)
        else:
            self.rect.move_ip(0, -(self.speed * time_passed))

class Fireball (pygame.sprite.Sprite):

    container = pygame.sprite.Group()

    def __init__ (self, image, speed, damage=1, player=None):
        pygame.sprite.Sprite.__init__ (self, self.container)


        self.image = image
        self.rect = self.image.get_rect()
        self.radias = ((self.rect.width/2 + self.rect.height/2)/2)
        self.speed = speed
        self.damage = damage
        self.player = player

    def update (self, time_passed):

        self.pos = (math.sin(self.angle) * self.speed * time_passed,
                    math.cos(self.angle) * self.speed * time_passed)
        self.rect.move_ip(self.pos)
        if self.rect.bottom < 0:   self.kill()
        if self.rect.top > 2000:   self.kill()
        if self.rect.left < 0:     self.kill()
        if self.rect.right > 2000: self.kill()

    def explode (self):

        Sparks(self.rect.center)
        if self.player:
            self.player.shots_hit[1] += 1


