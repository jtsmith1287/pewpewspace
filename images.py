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
DRONE_IMAGE    = pygame.image.load(p+"enemy.png").convert_alpha()
BOMBER_IMAGE   = pygame.image.load(p+"bomber.png").convert_alpha()
WARSHIP_IMAGE  = pygame.image.load(p+"warship.png").convert_alpha() 
FIREBALL_IMAGE = pygame.image.load(p+"fireball.png").convert_alpha()

# Passives
SMOKE_IMAGE    = pygame.image.load(p+"smoke.png").convert_alpha()
FIRE_IMAGE     = pygame.image.load(p+"fire.png").convert_alpha()
NUKE_IMAGE     = pygame.image.load(p+"nuke.png").convert_alpha()

# Player stuff
SHIP_IMAGE     = pygame.image.load(p+"spaceship.png").convert_alpha()
SHIP_IMAGE_TP  = pygame.image.load(p+"spaceship_transparent.png").convert_alpha()
LASER_IMAGE    = pygame.image.load(p+"laser_red.png").convert_alpha()

# Powerups
BULLET_IMAGE   = pygame.image.load(p+"bullet.png").convert_alpha()
WRENCH_IMAGE   = pygame.image.load(p+"wrench.png").convert_alpha()

# Animated images
MISSILE_IMAGE  = ss(p+"missile.png").images_at([(0,0,12,30), (13,0,8,30)])
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
BACKGROUNDS = ["stars_bg.png", "stars_bg_1.png", "stars_bg_2.png"]
