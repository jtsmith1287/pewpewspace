'''
Created on Jan 23, 2013

@author: Justin
'''

import pygame
from pygame.locals import *
from images import *

####################
# BASIC BLANK MENU #
####################
class Menu (pygame.sprite.Sprite):

    container = pygame.sprite.Group()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
    sfont = pygame.font.SysFont(pygame.font.get_default_font(), 15)

    def __init__ (self):
        pygame.sprite.Sprite.__init__ (self, self.container)
        self.running = True
        self.image = MENU
        self.rect = self.image.get_rect()
        # Menu widget containers
        self.widgets = pygame.sprite.Group()
        # Menu text containers
        self.text = pygame.sprite.RenderPlain()
        self.button_list = []
        self.pressed_button = None
        self.clock = pygame.time.Clock()

    def drawWidgets (self):

        pass

    def drawStuff (self):

        pass

    def checkButtonPress (self):

        if pygame.mouse.get_pressed()[0]:
            for button in self.button_list:
                if button.checkPressed(pygame.mouse.get_pos()):
                    self.pressed_button = button
        else:
            if self.pressed_button:
                self.pressed_button.unpress(pygame.mouse.get_pos())
                self.pressed_button = None

    def plainText (self, text, color=(255,255,255), small=False):

        if not small:
            return self.font.render(text, True, color)
        else:
            return self.sfont.render(text, True, color)

    def label (self, surface):

        return

    def run(self):

        self.drawWidgets()
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                self.checkButtonPress()
                if event.type == QUIT:
                    self.running = False
                    Menu.game.running = False
                if event.type == KEYDOWN:
                    if event.key == K_p or event.key == K_ESCAPE:
                        self.running = False
                        Menu.game.clock = pygame.time.Clock()
            Menu.container.draw(Menu.game.screen)
            self.drawStuff()
            pygame.display.flip()

class Button (pygame.sprite.Sprite):

    def __init__ (self, images, position, menu, text=None):
        pygame.sprite.Sprite.__init__(self, menu.__dict__["widgets"])

        self.unpressed = images[0]
        self.menu = menu
        self.image = self.unpressed
        self.pressed = images[1]
        self.rect = self.image.get_rect()
        self.is_pressed = False
        self.rect.center = position
        if text: # Must be surface object
            ButtonText(text, self, menu)

    def pressed_function (self):

        pass

    def unpress_function (self):

        pass

    def checkPressed (self, mouse_pos, pressed=False):

        if self.rect.collidepoint(mouse_pos) and not self.is_pressed:
            try:
                self.image = self.pressed
            except AttributeError:
                pass
            self.is_pressed = True
            self.pressed_function()
            return True

    def unpress (self, mouse_pos):

        if self.rect.collidepoint(mouse_pos) and self.is_pressed:
            try:
                self.image = self.unpressed
            except AttributeError:
                pass
            self.is_pressed = False
            self.unpress_function()
        else:
            self.image = self.unpressed
            self.is_pressed = False


class Slider (Button):

    def __init__ (self, image, position, bar, menu):
        Button.__init__(self, image, position, menu)
        self.bar = bar

    def function (self):

        pass


class ButtonText (pygame.sprite.Sprite):
    def __init__ (self, surface, button, menu):
        pygame.sprite.Sprite.__init__(self, menu.__dict__["text"])
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = button.rect.center
class Label (pygame.sprite.Sprite):
    def __init__ (self, surface, position, menu):
        pygame.sprite.Sprite.__init__(self, menu.__dict__["text"])
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = position


######################
# MAIN MENU CONTENTS #
######################
class MainMenu (Menu):

    def __init__ (self, game):
        Menu.__init__ (self)
        Menu.game = game
        self.rect.center = (Menu.game.screensize[0]/2, Menu.game.screensize[1]/2)

    def drawStuff (self):

        self.widgets.draw(Menu.game.screen)
        self.text.draw(Menu.game.screen)

    def drawWidgets (self):

        b = self.button_list
        spacer = 50
        surface = self.plainText("Quit Game")
        b.append(QuitButton((BUTT_WIDE, BUTT_WIDE_PRES),
                    (self.rect.center[0], self.rect.top+100), self, surface))
        surface = self.plainText("I'm Broken")
        next_pos = (b[0].rect.center[0], b[0].rect.bottom + spacer)
        b.append(OptionButton((BUTT_WIDE, BUTT_WIDE_PRES),
                              next_pos, self, surface))
        surface = self.plainText("Upgrades")
        next_pos = (b[1].rect.center[0], b[1].rect.bottom + spacer)
        b.append(UpgradeButton((BUTT_WIDE, BUTT_WIDE_PRES),
                              next_pos, self, surface))

class QuitButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        Menu.game.menu.running = False
        Menu.game.running = False


class OptionButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        self.menu = OptionMenu()
        self.menu.run()


class UpgradeButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        self.menu = UpgradeMenu()
        self.menu.run()

########################
# OPTION MENU CONTENTS #
########################
class OptionMenu (Menu):

    def __init__ (self):
        Menu.__init__(self)

        self.rect.center = (Menu.game.screensize[0]/2, Menu.game.screensize[1]/2)

    def drawWidgets (self):

        surface = self.plainText("Volume", (0,0,0))
        Label(surface, (self.rect.center[0], self.rect.top+100), self)
        self.button_list.append(Slider((BUTT_WIDE, BUTT_WIDE_PRES),
                                       self.rect.center,
                                       self,
                                       surface))
    def drawStuff (self):

        self.widgets.draw(Menu.game.screen)
        self.text.draw(Menu.game.screen)

#########################
# UPGRADE MENU CONTENTS #
#########################
class UpgradeMenu (Menu):

    def __init__ (self):
        Menu.__init__(self)

        self.rect.center = (Menu.game.screensize[0]/2, Menu.game.screensize[1]/2)

    def drawWidgets (self):

        spacer = 50
        b = self.button_list
        surface = self.plainText("Upgrades", (0,0,0))
        Label(surface, (self.rect.center[0], self.rect.top+50), self)
        surface = self.plainText(
            "Points: %s" %(Menu.game.player.ranks["remaining"]), (0,0,0))
        surface = pygame.transform.smoothscale(surface, (60, 20))
        Label(surface, (self.rect.center[0]+150, self.rect.top+50), self)

        surface = self.plainText("Hammer")
        next_pos = (self.rect.left + 140, self.rect.top + spacer*2)
        b.append(HammerButton((BUTT_WIDE, BUTT_WIDE_PRES),
                                   next_pos, self, surface))
        surface = self.plainText("Next: %s" %(
            RANK_DESC["hammer"][Menu.game.player.ranks["hammer"]]),(0,0,0),True)
        Label(surface, (next_pos[0] + 250, next_pos[1]), self)

        surface = self.plainText("Sabre")
        next_pos = (b[0].rect.center[0], b[0].rect.bottom + spacer)
        b.append(SabreButton((BUTT_WIDE, BUTT_WIDE_PRES),
                             next_pos, self, surface))
        surface = self.plainText("Next: %s" %(
            RANK_DESC["sabre"][Menu.game.player.ranks["sabre"]]),(0,0,0),True)
        Label(surface, (next_pos[0] + 250, next_pos[1]), self)

        surface = self.plainText("Scorpion")
        next_pos = (b[1].rect.center[0], b[1].rect.bottom + spacer)
        b.append(ScorpionButton((BUTT_WIDE, BUTT_WIDE_PRES),
                             next_pos, self, surface))
        surface = self.plainText("Next: %s" %(
            RANK_DESC["scorpion"][Menu.game.player.ranks["scorpion"]]),(0,0,0),True)
        Label(surface, (next_pos[0] + 250, next_pos[1]), self)

        surface = self.plainText("Forge")
        next_pos = (b[2].rect.center[0], b[2].rect.bottom + spacer)
        b.append(ForgeButton((BUTT_WIDE, BUTT_WIDE_PRES),
                             next_pos, self, surface))
        surface = self.plainText("Next: %s" %(
            RANK_DESC["forge"][Menu.game.player.ranks["forge"]]),(0,0,0),True)
        Label(surface, (next_pos[0] + 250, next_pos[1]), self)


    def drawStuff (self):

        self.widgets.draw(Menu.game.screen)
        self.text.draw(Menu.game.screen)

class HammerButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        player = Menu.game.player
        ranks = player.ranks
        current_rank_line = ranks["hammer"] % 4
        if ranks["remaining"] > 0 and ranks["hammer"] < 16:
            if current_rank_line == 0:            # Armor Plating Increase
                player.damage_res -= 0.1
                if (8 - ranks["hammer"]) < 2:
                    player.damage_res -= 0.1
            elif current_rank_line == 1:          # Missile Damage Increase
                player.missile_damage += 2
                if (8 - ranks["hammer"]) < 2:
                    player.missile_damage = 30
            elif current_rank_line == 2:          # Nuke construction speed
                player.points_until_nuke *= 0.9
            elif current_rank_line == 3:          # Nuke damage
                player.nuke_damage += 50
            ranks["remaining"] -= 1
            ranks["hammer"] += 1

        print ("DR %s\n"
                "M. Damage %s\n" %(player.damage_res, player.missile_damage))

        # Refresh the menu
        self.menu.widgets = pygame.sprite.Group()
        self.menu.text = pygame.sprite.RenderPlain()
        self.menu.drawWidgets()


class SabreButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        player = Menu.game.player
        ranks = player.ranks
        current_rank_line = ranks["sabre"] % 4
        if ranks["remaining"] > 0 and ranks["sabre"] < 11:
            if current_rank_line == 0:         # Reload Speed
                player.reload_speed -= 1
            elif current_rank_line == 1:       # Player Speed
                player.speed += 10
            elif current_rank_line == 2:       # Laser Speed
                player.laser_speed += 200
            elif current_rank_line == 3:       # Gun count  
                player.guns += 1

            ranks["remaining"] -= 1
            ranks["sabre"] += 1

        print ("Reload %s\n"
                "Speed %s\n"
                "Laser Speed %s"
                "Gun count %s\n" %(player.reload_speed,
                                   player.speed,
                                   player.laser_speed,
                                   player.guns))

        # Refresh the menu
        self.menu.widgets = pygame.sprite.Group()
        self.menu.text = pygame.sprite.RenderPlain()
        self.menu.drawWidgets()

class ScorpionButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        player = Menu.game.player
        ranks = player.ranks
        current_rank_line = ranks["scorpion"] % 3
        if ranks["remaining"] > 0 and ranks["scorpion"] < 12:
            if current_rank_line == 0:           # Player Damage
                player.damage += 0.1
                if (8 - ranks["scorpion"]) < 3:
                    player.damage += 0.1
            elif current_rank_line == 1:         # EMP stuff
                if player.emp:
                    player.emp["timer"][1] = 1
                    player.emp["duration"][0] += 2
                else:
                    player.emp = {"timer": [60,0.1], "duration":[5,0]}
            elif current_rank_line == 2:         # Missile Speed
                player.missile_speed += 100

            ranks["remaining"] -= 1
            ranks["scorpion"] += 1

        print ("Damage %s\n"
                "Missile Speed %s\n"
                 %(player.damage, player.missile_speed))

        # Refresh the menu
        self.menu.widgets = pygame.sprite.Group()
        self.menu.text = pygame.sprite.RenderPlain()
        self.menu.drawWidgets()

class ForgeButton (Button):

    def __init__ (self, images, position, menu, text):
        Button.__init__(self, images, position, menu, text)

    def unpress_function (self):

        player = Menu.game.player
        ranks = player.ranks
        current_rank_line = ranks["forge"] % 1
        if ranks["remaining"] > 0 and ranks["forge"] < 4:
            if current_rank_line == 0:          # Missile reload timer
                print player.missile_timer
                if player.missile_timer[0] == 30:
                    player.missile_timer[0] = 15
                else:
                    player.missile_timer[0] -= 10
                
            ranks["remaining"] -= 1
            ranks["forge"] += 1
                

        print ("Missile Timer %s\n" %(player.missile_timer[0]))

        # Refresh the menu
        self.menu.widgets = pygame.sprite.Group()
        self.menu.text = pygame.sprite.RenderPlain()
        self.menu.drawWidgets()

RANK_DESC = {"hammer": ["Increase armor plating to 110%",
                        "Missile damage to 120%",
                        "Nuke construction speed down 10%",
                        "Nuke damage at 150%",
                        "Increase armor plating to 120%",
                        "Missile damage to 140%",
                        "Nuke construction speed down 18%",
                        "Nuke damage at 200%",
                        "Increase armor plating to 130%",
                        "Missile damage to 160%",
                        "Nuke construction speed down 26%",
                        "Nuke damage at 250%",
                        "Increase armor plating to 150%",
                        "Missile damage to 300%",
                        "Nuke construction speed down 35%",
                        "Nuke damage at 300%",
                        "Upgrade line at maximum!"],
             "sabre": ["Reload speed efficiency to 5%",
                       "Movement speed to 106%",
                       "Laser velocity to 127%",
                       "Install additional laser",
                       "Reload speed efficiency to 12%",
                       "Movement speed to 111%",
                       "Laser velocity to 143%",
                       "Install third laser",
                       "Reload speed efficiency to 18%",
                       "Movement speed to 117%",
                       "Laser velocity to 153%",
                       "Upgrade line at maximum!"],
            "scorpion": ["Laser damage to 110%",
                         "Missile speed to 123%",
                         "Install EMP",
                         "Laser damage to 120%",
                         "EMP recharge - Seven second duration",
                         "Missile speed to 137%",
                         "Laser damage to 130%",
                         "EMP recharge - Nine second increased duration",
                         "Missile speed to 147%",
                         "Laser damage to 150%",
                         "EMP recharge - Eleven second increased duration",
                         "Missile speed to 154%",
                         "Upgrade line at maximum!"],
            "forge": ["Missile construction speed to 50 seconds",
                      "Missile construction speed to 40 seconds",
                      "Missile construction speed to 30 seconds",
                      "Missile construction speed to 15 seconds",
                      "Upgrade line at maximum!"]}                         
