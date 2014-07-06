""" Created on Jan 19, 2013

@author: Justin """

import pygame,os
from spritehandler import Spritesheet as ss

if os.name == "posix":
    p = os.path.join("images/")
elif os.name == "nt":
    p =  os.path.join("images\\")
else:
    print "Your operating system isn't gonna play this, sorry."
    raise SystemExit

# Enemies
BOSS_IMAGE     = pygame.image.load(p+"boss.png").convert_alpha()
BOSS_SHIELD    = pygame.image.load(p+"boss_shield.png").convert_alpha()
BOSS_GUARDIAN  = pygame.image.load(p+"boss_guard.png").convert_alpha()
DRONE_IMAGE    = pygame.image.load(p+"enemy.png").convert_alpha()
DRONE_IMAGE_2  = pygame.image.load(p+"enemy_2.png").convert_alpha()
DRONE_IMAGE_3  = pygame.image.load(p+"enemy_3.png").convert_alpha()
BOMBER_IMAGE   = pygame.image.load(p+"bomber.png").convert_alpha()
WARSHIP_IMAGE  = pygame.image.load(p+"warship.png").convert_alpha() 
FIREBALL_IMAGE = pygame.image.load(p+"fireball.png").convert_alpha()
BOSS_BULLET_IMAGE = pygame.image.load(p+"boss_bullets.png").convert_alpha()

# Enemies @ "next level"
BOSS_IMAGE_n     = pygame.image.load(p+"boss_n.png").convert_alpha()
BOSS_GUARDIAN_n  = pygame.image.load(p+"boss_guard_n.png").convert_alpha()
DRONE_IMAGE_n    = pygame.image.load(p+"enemy_n.png").convert_alpha()
DRONE_IMAGE_2_n  = pygame.image.load(p+"enemy_2_n.png").convert_alpha()
DRONE_IMAGE_3_n  = pygame.image.load(p+"enemy_3_n.png").convert_alpha()
BOMBER_IMAGE_n   = pygame.image.load(p+"bomber_n.png").convert_alpha()
WARSHIP_IMAGE_n  = pygame.image.load(p+"warship_n.png").convert_alpha() 
FIREBALL_IMAGE_n = pygame.image.load(p+"fireball_n.png").convert_alpha()

# Passives
SMOKE_IMAGE    = pygame.image.load(p+"smoke.png").convert_alpha()
FIRE_IMAGE     = pygame.image.load(p+"fire.png").convert_alpha()
NUKE_IMAGE     = pygame.image.load(p+"nuke.png").convert_alpha()

# Player stuff
SHIP_IMAGE     = pygame.image.load(p+"spaceship.png").convert_alpha()
SHIP_IMAGE_TP  = pygame.image.load(p+"spaceship_transparent.png").convert_alpha()
LASER_IMAGE    = pygame.image.load(p+"laser_red.png").convert_alpha()
LASER_IMAGE_2    = pygame.image.load(p+"laser_2.png").convert_alpha()
LASER_IMAGE_3   = pygame.image.load(p+"laser_3.png").convert_alpha()
LASER_IMAGE_4    = pygame.image.load(p+"laser_4.png").convert_alpha()
LASER_IMAGE_5    = pygame.image.load(p+"laser_5.png").convert_alpha()

# Powerups
BULLET_IMAGE   = pygame.image.load(p+"bullet.png").convert_alpha()
WRENCH_IMAGE   = pygame.image.load(p+"wrench.png").convert_alpha()
POWERUP_GLOW   = pygame.image.load(p+"powerup_glow.png").convert_alpha()

# Animated images
MISSILE_IMAGE  = ss(p+"missile.png").images_at([(0,0,20,32), (20,0,20,32)])
WARP_IMAGE     = ss(p+"warp.png", (40,40), 2,5).images_at()
SPARKS1_IMAGE   = ss(p+"sparks.png", (50,50), 4,4).images_at()
SPARKS2_IMAGE   = ss(p+"sparks.png", (50,50), 4,4).images_at()
M_EXPLOSION_1  = ss(p+"explosionsheet1.png", (130,130), 5,5).images_at()
M_EXPLOSION_2  = ss(p+"explosionsheet2.png", (100,100), 9,8).images_at()

# Menu
# Naming scheme: 4 letters per tag
#    OBJECT _ SIZE _ STATE
MENU           = pygame.image.load(p+"menu.png").convert_alpha()
BUTT_SMAL      = pygame.image.load(p+"button_small.png").convert_alpha()
BUTT_SMAL_PRES = pygame.image.load(p+"button_small_pressed.png").convert_alpha()
BUTT_WIDE      = pygame.image.load(p+"button_wide.png").convert_alpha()
BUTT_WIDE_PRES = pygame.image.load(p+"button_wide_pressed.png").convert_alpha()

# Self explanatory 
BACKGROUNDS = ["stars_bg.png", 
               "stars_bg_1.png",
               "stars_bg_2.png",
               "stars_bg_3.png",
               "stars_bg_4.png"]
