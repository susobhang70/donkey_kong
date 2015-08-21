import pygame
from constants import *

#----------------------Objects with Text-------------------------------------#

def text_objects(text, font):
    """Returns image surfaces and rectangles of text objects"""
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#----------------------------------------------------------------------------#

#------------------Checking where a point lies wrt boundaries----------------#

def checkWall(checkX, checkY, width, height, wallxh = WALLX_HIGHER, wallxl = \
    WALLX_LOWER, wallyh = WALLY_HIGHER, wallyl = WALLY_LOWER):
    """Check if cords are inside the boundaries given as parameters"""
    #check if x cord is inside the boundaries
    if checkX + width < wallxh and checkX > wallxl:
        #check if y cord is inside the boundaries
        if checkY + height< wallyh and checkY > wallyl:
            return 1
        #check if y cord is on vertical boundary
        elif checkY + height == wallyh or checkY == wallyl:
            return 2
        else:                                               #outside
            return 0
    #check if x cord is on the horizontal boundary
    elif checkX + width == wallxh or checkX == wallxl:
        #cord is on the corners
        if checkY + height == wallyh or checkY == wallyl:
            return 3
        #cord is on the horizontal border
        else:
            return 4
    else:                                                   #outside
        return 0

#----------------------------------------------------------------------------#

#-----------------------Draw rectange and return object----------------------#

def drawRect(screen, x, y, w, h, color, thick = 0):
    """Draws a rectange and returns its object"""
    myrect = pygame.Rect(x, y, w, h)                        #rectange object
    pygame.draw.rect(screen, color, myrect, thick)
    return myrect

#----------------------------------------------------------------------------#
