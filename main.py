'''
Created on Jan 7, 2013

@author: Justin
'''

print "Importing assets..."
import pygame,sys
pygame.mixer.pre_init(22050,-16, 2, 256)
pygame.init() # TODO: Catch exceptions for load failures
screen = pygame.display.set_mode((800,900))

from pygame.locals import *

from random import choice
from spaceship import SpaceShip,Fireball,Missile
from passive import ScrollingBackground,Passive,Background,HealthBar,PowerUpGlow
from enemy import Drone,Enemy,EnemyFireball,Boss,Warship,Bomber
from powerup import PowerUp,Wrench,Bullet,MissileReload,GunUpgrade
from animation import Animation
from sounds import sfx

from random import randint
from images import *

from menu import MainMenu
print "Assets imported"



class Game:

    def __init__ (self):

        self.screensize   = self.assembleImages()
        self.screen       = pygame.display.set_mode(self.screensize, 0, 32)
        self.volume       = 0.5
        self.player       = SpaceShip(self.screensize)
        HealthBar(self.player, self.screen, True)
        self.clock        = pygame.time.Clock()
        self.level        = 1
        self.boss         = None
        self.font         = pygame.font.Font("GearsOfPeace.ttf", 12)
        self.med_font     = pygame.font.Font("GearsOfPeace.ttf", 30)
        self.big_font     = pygame.font.Font("GearsOfPeace.ttf", 50)
        self.notify       = {"msg": None, "timer": [60*3, 0]}
        self.spawner      = {"max_enemies": 2,
                             "enemy_killed": 0,
                             "spawn_delay": (60 * 2.2),
                             "spawn_counter": 0,
                             "boss_out": False,}
        self.running = True

    def openingScene (self):

        to_play = [sfx.AI_greeting, sfx.AI_mission]
        running = True
        for index, sound in enumerate(to_play):
            sound.play()
            while running:
                self.time_passed = self.clock.tick(60)/1000.0
                if not pygame.mixer.get_busy():
                    break
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        self.running = False
                        return
                    if event.type == KEYDOWN and event.key == K_ESCAPE:
                        running = False
                        sound.stop()
                        return
                
                self.manageSprite(Background.container)
                text = "SPACEBAR = FIRE ZE LASERS"
                surface = self.font.render(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]/2-120, 250))
                text = "M = FIRE A MISSILE"
                surface = self.font.render(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]/2-120, 280))
                text = "N = LAUNCH NUCLEAR WARHEAD"
                surface = self.font.render(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]/2-120, 310))
                text = "E = EMP (Scorpion Upgrade Line)"
                surface = self.font.render(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]/2-120, 340))
                text = "R = Repair (Collect Wrenches)"
                surface = self.font.render(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]/2-120, 370))
                text = "PRESS Esc TO SKIP INTRO"
                surface = self.med_font.render(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]/2-250, 450))
                self.manageSprite(self.player.container)
                pygame.display.flip()


    def assembleImages(self):

        image_path = os.path.join("backgrounds", choice(BACKGROUNDS))

        backgroundTL = ScrollingBackground(image_path)
        backgroundBL = ScrollingBackground(image_path)
        backgroundTL.rect.bottom = backgroundBL.rect.top
        width = backgroundTL.rect.width
        height = backgroundTL.rect.height

        global screenrect
        screenrect = Rect(0,0,backgroundTL.rect.width,backgroundTL.rect.height)
        display = pygame.display.Info()
        if display.current_h < 1000:
            height = display.current_h 
        return (width, height)

    def manageSprite (self, container):

        container.update(self.time_passed)
        container.draw(self.screen)

    def spawnEnemies (self):

        spwn = self.spawner
        if spwn["spawn_counter"] >= spwn["spawn_delay"]:
            if len(Enemy.container) < spwn["max_enemies"]:
                if self.level -3 in range(3):
                    enemy = choice([Drone, Warship])(self.screensize,
                                                     self.player,
                                                     self.level)
                elif self.level > 6:
                    enemy = choice([Drone, Warship, Bomber])(self.screensize, 
                                                             self.player, 
                                                             self.level)
                else:
                    enemy = Drone(self.screensize, self.player, self.level)
                if self.level > 10:
                    enemy.armor["T"] *= 2
                    enemy.armor["M"] *= 2
                HealthBar(enemy, self.screen)
                spwn["spawn_counter"] = 0
        else:
            if not spwn["boss_out"]:
                spwn["spawn_counter"] += 1

        if spwn["enemy_killed"] >= spwn["max_enemies"]+(
                5+self.level*3) and (spwn["boss_out"] == False):
            sfx.stab.play()
            self.boss = Boss(self.screensize, self.player, self.level)
            self.boss.rect.midbottom = (self.screensize[0]/2, 0)
            spwn["enemy_killed"] = 0
            spwn["boss_out"] = True
            spwn["max_enemies"] += 1
            HealthBar(self.boss, self.screen)

    def gameOver (self):

        # Do all the game over stuff here...
        self.running = False # True for debugging purposes - set to False to end game

    def playerDamage (self, enemy, projectiles):

        for proj in projectiles:
            proj.explode()
            if enemy.decreaseHealth(proj.damage) <= 0:
                if type(enemy).__name__ == "Guard":
                    self.boss.guards_out -= 1
                    self.player.exp += enemy.armor["M"]
                    enemy.die(sfx.muffled_explosion)
                    return
                self.spawner["enemy_killed"] += 1
                if type(enemy).__name__ == "Drone":
                    self.player.exp += enemy.armor["M"]+1
                else:
                    self.player.exp += enemy.armor["M"]
                chance = randint(1,13)
                if chance in [12, 13]:
                    new_powerup = Wrench()
                    new_powerup.rect.center = enemy.rect.center
                    PowerUpGlow(new_powerup)
                elif chance == 2:
                    new_powerup = Bullet()
                    new_powerup.rect.center = enemy.rect.center
                    PowerUpGlow(new_powerup)
                elif chance == 3:
                    new_powerup = MissileReload()
                    new_powerup.rect.center = enemy.rect.center
                    PowerUpGlow(new_powerup)
                elif chance == 4:
                    new_powerup = GunUpgrade()
                    new_powerup.rect.center = enemy.rect.center
                    PowerUpGlow(new_powerup)
                enemy.die(sfx.muffled_explosion)
                break

    def collisionCheck (self, collide):

        # Check if the player has shot an enemy (non boss)
        kpow = collide(Enemy.container, Fireball.container, False, True)
        if kpow:
            for enemy in kpow:
                self.playerDamage(enemy, kpow[enemy])
        # Check if an enemy has shot the player
        boom = collide(EnemyFireball.container, self.player.container, True, False)
        if boom:
            if self.player.decreaseHealth(1) <= 0:
                self.player.die()
        # Check if the player crashed into an enemy
        bang = collide(Enemy.container, self.player.container, False, False)
        if bang:
            for enemy in bang:
                e_armor = enemy.armor["T"]
                if type(enemy).__name__ == "Guard":
                    self.boss.guards_out -= 1
                enemy.die(sfx.muffled_explosion)
                if self.player.decreaseHealth(e_armor) <= 0:
                    self.player.die()
        # Check if the player has shot a boss
        bash = collide(Fireball.container, Boss.container, True, False)
        if bash:
            for projectile in bash:
                if not self.boss.invincible:
                    if self.boss.decreaseHealth(projectile.damage) <= 0:
                        self.spawner["boss_out"] = False
                        self.player.exp += self.boss.armor["M"]
                        self.level += 1
                        self.boss.die(sfx.muffled_explosion)
                        self.boss = None
                        self.player.ranks["remaining"] += 1
                        text = "New Upgrades! (Press ESC)"
                        self.notify["msg"] = self.med_font.render(text, True, (255,255,255))
                        break
                    projectile.explode()
        # Check if the player has grabbed a PowerUp
        ding = collide(PowerUp.container, self.player.container, True, False)
        if ding:
            for power in ding:
                power.effect(self.player)

    def showStats (self):

        fr = self.font.render
        if self.player.lives < 0:
            text = "Game Over..."
            surface = self.big_font.render(text, True, (255,255,255))
            self.screen.blit(surface, (200, self.screensize[1]/2-75))
            text = "EXP: %s -- LEVEL: %s" %(game.player.exp, game.level)
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (350, self.screensize[1]/2))
        else:
            text = "Level: %s" %(game.level)
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (10, 10))
            text = "EXP: %s" %(int(round(game.player.exp)))
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (10, 30))
            text = "Escape Pods: %s" %(game.player.lives)
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (10, 50))
            text = game.player.getHitPercentage()
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (10, 70))
            text = "Armor: %s/%s" % (game.player.armor["T"], game.player.armor["M"])
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (10, self.screensize[1]-50))
            text = "Missiles: %s" %(self.player.missiles)
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (self.screensize[0]-180, 10))
            text = "Repair Drones: %s" %(self.player.wrenches)
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (self.screensize[0]-180, 30))
            text = "Nukes: %s" %(game.player.nukes)
            surface = fr(text, True, (255,255,255))
            self.screen.blit(surface, (self.screensize[0]-180, 50))
            if self.player.missile:
                text = "NEXT MISSILE: 0:%s" %(round(game.player.missile_timer[1],1))
                surface = fr(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]-180, 70))
            if self.player.emp:
                text = "NEXT EMP: 0:%s" %(round(game.player.emp["timer"][1],1))
                surface = fr(text, True, (255,255,255))
                self.screen.blit(surface, (self.screensize[0]-180, 90))


    def displayNotifications (self):

        if not self.notify["msg"]: return
        if self.notify["timer"][1] >= self.notify["timer"][0]:
            self.notify["msg"] = None
            self.notify["timer"][1] = 0
        else:
            self.screen.blit(self.notify["msg"], (275, int(self.screensize[1]/3-50)))
            self.notify["timer"][1] += 1

    def eventCheck(self, event):

        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN:
            if event.key == K_p or event.key == K_ESCAPE: # Pause the game and open the menu
                self.menu = MainMenu(self)
                self.menu.run()
            if event.key == K_SPACE:
                self.player.shooting = True
            if event.key == K_UP:
                self.player.moving.add("forward")
            if event.key == K_DOWN:
                self.player.moving.add("back")
            if event.key == K_RIGHT:
                self.player.moving.add("right")
            if event.key == K_LEFT:
                self.player.moving.add("left")
            if event.key == K_e:
                if self.player.emp:
                    self.player.triggerEmp(self.screen, Enemy.container, self.boss)
            if event.key == K_m:
                self.player.missile(Enemy.container, self.boss)
            if event.key == K_n:
                self.player.nuke(self.screen, Enemy.container, self.boss)
            if event.key == K_r:
                self.player.repair()
            if event.key == K_EQUALS:
                self.volume += 0.1
                if self.volume > 1:
                    self.volume = 1.0
                pygame.mixer.music.set_volume(self.volume)
            if event.key == K_MINUS:
                self.volume -= 0.1
                if self.volume < 0:
                    self.volume = 0.0
                pygame.mixer.music.set_volume(self.volume)
        if event.type == KEYUP:
            if event.key == K_SPACE:
                self.player.shooting = False
            if event.key == K_UP:
                self.player.moving.remove("forward")
            if event.key == K_DOWN:
                self.player.moving.remove("back")
            if event.key == K_RIGHT:
                self.player.moving.remove("right")
            if event.key == K_LEFT:
                self.player.moving.remove("left")

    def run (self):

        #self.notify["msg"] = self.med_font.render("Pew Pew Space", True, (255,255,255))
        self.openingScene()

        sfx.play_music()
        collide = pygame.sprite.groupcollide

        while self.running:
            self.time_passed = self.clock.tick(60)/1000.0
            pygame.display.set_caption("[FPS -- %s]" %(int(self.clock.get_fps())))
            for event in pygame.event.get():
                self.eventCheck(event)

            self.spawnEnemies()
            self.manageSprite(Background.container)           # Background
            self.showStats()                                  # Stats
            self.displayNotifications()                       # Notifications
            self.manageSprite(Passive.container)              # Passive sprites
            self.manageSprite(Animation.container)            # Animations
            self.manageSprite(Fireball.container)             # Player's bullets
            self.manageSprite(Missile.container)              # Player missiles
            self.manageSprite(Boss.container)                 # Boss
            self.manageSprite(EnemyFireball.container)        # Enemy's bullets
            self.manageSprite(Enemy.container)                # Enemies
            self.manageSprite(HealthBar.container)            # Healthbars
            self.manageSprite(PowerUp.container)              # PowerUps
            self.manageSprite(self.player.container)          # Player
            self.collisionCheck(collide)                      # Collisions
            pygame.display.flip()                             # Update dislplay


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    try:
        sys.exit()
    except: SystemExit()

