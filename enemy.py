from __future__ import division
import pygame, math
from random import randint,uniform,choice
from spaceship import Fireball
from animation import Explosion
from passive import BossShield
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

    def __init__ (self, size, player ,level):
        pygame.sprite.Sprite.__init__ (self, Enemy.container)

        if level < 10:
            self.image = choice([DRONE_IMAGE, DRONE_IMAGE_2, DRONE_IMAGE_3])
        else:
            self.image = choice([DRONE_IMAGE_n, DRONE_IMAGE_2_n, DRONE_IMAGE_3_n])
        self.rect = self.image.get_rect()
        self.rect.center = (randint((0+150),(size[0]-150)),
                            randint((0+50),(size[1]-500)))
        self.angle = uniform(0, math.pi*2)
        self.invincible = False
        Warp(self.rect.center)
        self.disabled = False
        self.the_enemy = player

        self.armor = {"T": 1.2, "M": 1.2} # T = Total, M = Max
        self.speed = randint(150, 300)
        self.reload_speed = randint(12, 30)
        self.reload_time = self.reload_speed

    def shoot (self):

        bullet = Fireball(FIREBALL_IMAGE, 325)
        Fireball.container.remove(bullet)
        EnemyFireball.container.add(bullet)
        bullet.angle = math.pi*2
        bullet.rect.midtop = self.rect.midbottom
        sfx.enemy_shot.play()

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

        if self.rect.right > 850:
            self.angle = - self.angle
        elif self.rect.left < -50:
            self.angle = - self.angle
        if self.rect.bottom > 850:
            self.angle = math.pi - self.angle
        elif self.rect.top < -50:
            self.angle = math.pi - self.angle

    def varySpeed(self):
        
        pass

    def update (self, time_passed):

        self.varySpeed()
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

    def __init__ (self, size, player, level):
        pygame.sprite.Sprite.__init__ (self, Enemy.container)

        if level < 10:
            self.image = BOMBER_IMAGE
        else:
            self.image = BOMBER_IMAGE_n
        self.rect = self.image.get_rect()
        self.rect.center = (randint((0+30),(size[0]-30)), 0)
        self.radias = ((self.rect.width/2 + self.rect.height/2)/2)
        self.direction = 1
        self.speed = 275
        self.destination = (size[0]-self.rect.center[0], size[1]+100)
        diff = (self.destination[0]-self.rect.center[0],
                self.destination[1]-self.rect.center[1])
        self.angle = math.atan2(diff[0], diff[1])
        self.reload_speed = [75, 10, 3] #Interval,delay,shots per burst
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
        sfx.enemy_shot.play()

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


class Guard (Drone):
    
    def __init__(self, size, player, level):
        Drone.__init__(self, size, player, level)
        
        self.speed_variance = (400, 500)
        self.speed_timer = [60, 0]
        self.armor["M"] = 5
        self.armor["T"] = 5
        if level < 10:
            self.image = BOSS_GUARDIAN
        else:
            self.image = BOSS_GUARDIAN_n
        self.rect = self.image.get_rect()
        
    def varySpeed(self):
        
        self.speed_timer[1] += 1
        # Time to change speeds again
        if self.speed_timer[1] >= self.speed_timer[0]:
            # Current speed "mode" is normal so we start moving quickly
            if self.speed <= self.speed_variance[0]:
                self.speed = randint(self.speed_variance[0], self.speed_variance[1])
            else:
                self.speed = randint(150, 250)
            self.speed_timer[0] = randint(30, 240)
            self.speed_timer[1] = 0


class Warship (Enemy):

    def __init__ (self, size, player, level):
        pygame.sprite.Sprite.__init__ (self, Enemy.container)

        if level < 10:
            self.image = WARSHIP_IMAGE
        else:
            self.image = WARSHIP_IMAGE_n
        self.rect = self.image.get_rect()
        self.rect.midbottom = (randint(30,size[0]-30), 0)
        self.radias = ((self.rect.width/2 + self.rect.height/2)/2)
        self.direction = 1
        self.invincible = False
        self.the_enemy = player
        self.armor = {"T": 8, "M": 8} # T = Total, M = Max
        self.disabled = False
        self.speed = 75
        self.reload_speed = int(60 * 3)
        self.reload_time = self.reload_speed
        self.gun_sep = self.rect.height/6

    def shoot (self, direction, time_passed):

        curr_gun = 0
        topleft = self.rect.topleft
        topright = self.rect.topright
        for shot in xrange(4):
            bullet = Fireball(FIREBALL_IMAGE, 325)
            Fireball.container.remove(bullet); EnemyFireball.container.add(bullet)
            if direction == "left":
                bullet.rect.center = (topleft[0], topleft[1]+curr_gun)
                bullet.angle = (math.pi*2) * 0.75
            else:
                bullet.rect.center = (topright[0], topright[1]+curr_gun)
                bullet.angle = (math.pi*2) * 0.25
            curr_gun += self.gun_sep
        sfx.warship_shot.play()

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

    def __init__ (self, size, player, level):
        pygame.sprite.Sprite.__init__(self, self.container)

        if level < 10:
            self.image = BOSS_IMAGE
        else:
            self.image = BOSS_IMAGE_n
        self.rect  = self.image.get_rect()
        self.direction = 1
        self.screen_size = size
        self.player = player
        self.radias = int((self.rect.width/2.3) + (self.rect.height/2.3)/2)
        self.shot_sound = sfx.boss_shot
        self.invincible = False

        # Dynamic variables based on power and/or level
        self.power = player.exp
        self.level = level
        self.speed = 125
        self.travelled = 0
        self.max_travel = 300
        self.directions = {"downright": (1, 1),
                           "right": (1, 0),
                           "backright": (-1, 0),
                           "left": (-1, 0),
                           "backleft": (1, 0),
                           "downleft": (-1, 1),
                           "down": (0, 1),
                           "backdownright": (-1, -1),
                           "backdownleft": (1, -1),
                           "backdown": (0, -1)}
        self.moving = None
        self.disabled = False
        self.guards_out = 0
        self.guards_spawned = False
        if self.level % 2 == 1:
            self.guards_out = -1

        armor = int((self.level*1.8)+(self.power/12)) + 50
        self.armor = {"T": armor, "M": armor} # T = Total, M = Max

    def shoot (self, shots, time_passed):

        self.shot_sound.play()
        angle = 0
        step = (math.pi*2)/shots
        for i in xrange(shots):
            bullet = Fireball(BOSS_BULLET_IMAGE, 350)
            bullet.angle = angle + (uniform(-.25,.25))
            bullet.pos = ((math.sin(bullet.angle) * bullet.speed) * time_passed,
                          (math.cos(bullet.angle) * bullet.speed) * time_passed)
            Fireball.container.remove(bullet)
            EnemyFireball.container.add(bullet)
            bullet.rect.center = (self.rect.center[0], self.rect.center[1]+40)
            angle += step

    def spawnGuards(self):
        
        if self.guards_out != -1 and not self.guards_spawned:
            sfx.guard_spawn.play()
            BossShield(self)
            self.guards_spawned = True
            self.invincible = True
            self.guards_out = 2 + int(self.level/2.0)
            positions = [int(self.screen_size[0]/self.guards_out) * i \
                         for i in range(self.guards_out + 1)][1:]
            for pos in range(self.guards_out):
                guard = Guard(self.screen_size, self.player, self.level)
                guard.rect.center = (positions[pos], 400)
            # Offset guards by one so last kill drops count to -1 instead of 0.
            # This prevents guards from being spawned more than once.
            self.guards_out -= 1
            
    def update (self, time_passed):

        if self.disabled: return

        # Move boss into position
        if self.rect.bottom < 300:
            self.rect.move_ip(0, int(self.speed*time_passed))
            return
        # If less than 20%, spawn guardians
        if float(self.armor["T"]) / float(self.armor["M"]) < 0.20:
            self.spawnGuards()
        # Guards are not present -- boss acts normally
        if (self.guards_spawned and self.guards_out <= -1) or (
            not self.guards_spawned):
            # Calculate chances to move and shoot
            chance = randint(1, 100-(self.level*2))
            if chance == 7:
                self.shoot(randint(self.level + 2,(self.level+10)), time_passed)
            if chance < 6 and self.moving == None:
                self.moving = choice(["right", "left", "downright", "downleft", "down"])
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
            # Reset invincibility.
            if self.invincible:
                self.invincible = False


