import pygame,os
from random import choice
pygame.mixer.init() # TODO: Catch exceptions for load failures
pygame.mixer.set_num_channels(50)

class Sfx (object):

    # TODO: Create permanent Channel() with set channels

    def __init__ (self):

        p = self.getOs()
        self.muffled_explosion = self.load_sound(p+"muffled_explosion.wav")
        self.blastershot       = self.load_sound(p+"blastershot.wav")
        self.boss_shot         = self.load_sound(p+"boss_shot.wav")
        self.missile_launch    = self.load_sound(p+"missile_launch.wav")
        self.repair            = self.load_sound(p+"repair.wav")
        self.epic_nuke         = self.load_sound(p+"epic_nuke.wav")

        # Dialogue
        self.AI_greeting = self.load_sound(p+"AI_greeting.wav")
        self.AI_mission = self.load_sound(p+"AI_mission.wav")
        self.AI_missile = self.load_sound(p+"AI_missile.wav")
        self.AI_nuke = self.load_sound(p+"AI_nuke.wav")
        self.AI_status = self.load_sound(p+"AI_repair.wav")
        self.AI_repair = self.load_sound(p+"AI_status.wav")
        # list of currently playing dialogue to prevent overlap
        self.sounds_playing = []

        # Misc
        self.stab = self.load_sound(p+"stab.wav")

        # Music
        self.music = ["theme.mp3"]
        self.combat_music = self.load_music(p+choice(self.music))

        self.setDefaultVolume()

    def getOs (self):

        if os.name == "posix":
            return os.path.join("sounds/")
        elif os.name == "nt":
            return os.path.join("sounds\\")
        else:
            print "Your operating system isn't gonna play this, sorry."
            raise SystemExit

    def setDefaultVolume (self, volume=0.5):

        d = self.__dict__
        skip = ["music", "AI_greeting", "AI_mission",
                "sounds_playing"]
        for key,sound in d.iteritems():
            if sound and key not in skip:
                sound.set_volume(volume)

        d[skip[1]].set_volume(0.9)
        d[skip[2]].set_volume(0.9)

    def setAllVolume (self, volume):

        d = self.__dict__
        skip = ["music"]
        for key,sound in d.iteritems():
            if sound and key not in skip:
                sound.set_volume(volume)

    def load_sound (self, filename):

        try:
            sound = pygame.mixer.Sound(filename)
        except pygame.error, msg:
            print msg, sound
            raise SystemExit

        return sound

    def load_music (self, filename):

        try:
            pygame.mixer.music.load(filename)
        except pygame.error, msg:
            print msg, filename
            raise SystemExit

    def play_music (self):

        pygame.mixer.music.play(-1)

sfx = Sfx()
