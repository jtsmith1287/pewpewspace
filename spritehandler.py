# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame

class Spritesheet (object):

    def __init__ (self, filename, frame_size=None, lines=1, columns=1):

        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.current_ckey = self.sheet.get_colorkey()
            self.frame_size = frame_size
            self.grid = (lines, columns)
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    # Load a specific image from a specific rectangle
    def image_at (self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"

        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey == None:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at (self, rects=None, colorkey=None):
        "Loads multiple images, supply a list of coordinates"

        if rects == None:
            rects = self.assembleCoords()
        return [self.image_at(rect, self.current_ckey) for rect in rects]


    # Load a whole strip of images
    def load_strip (self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"

        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def assembleCoords (self):

        coords = []
        w,h = self.frame_size
        for line in xrange(self.grid[0]):
            for frame in xrange(self.grid[1]):
                coords.append((frame*h, line*w, w, h))
        return coords
