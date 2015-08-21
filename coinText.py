import random
import pygame
from functions import *
from layout import *

#-------------------------Coins class----------------------------------------#
class coins(pygame.sprite.Sprite, Layout):
    """Defines methods and attributes of randomly generated coins"""
    def __init__(self, level):
        """Initializes coin for a level on a random floor"""
        super().__init__()
        Layout.__init__(self)
        #coin attributes
        self.__color = COIN_COLOR
        self.__level = level
        self.__width = COIN_WIDTH
        self.__height = COIN_HEIGHT
        #coin image
        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill(self.__color)

        #choose random floor for a coin
        self.__floor = random.randint(2, 5)
        #choose random coin position
        self.__x = random.randint(self.redx[self.__level][self.__floor], \
            self.redx[self.__level][self.__floor] + \
            self.redw[self.__level][self.__floor] - self.__width)
        self.__y = self.redy[self.__level][self.__floor] - self.__height
        self.__drawCoin()

    def __drawCoin(self):
        """Draws the coin object on the screen"""
        self.rect = drawRect(self.image, self.__x, self.__y, self.__width, \
            self.__height, self.__color)
        pygame.display.update()

#-----------------------------Coins Class end--------------------------------#

#-----------------------------Text class-------------------------------------#

class Text(pygame.sprite.Sprite):
    def __init__(self, text = " ", score = 0, color = green, width = 0, \
        height = 0):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.__font = pygame.font.SysFont("Arial", 25)
        self.__color = color
        self.__width = width
        self.__height = height
        self.__text = text
        self.__score = score
        self.__textSurf = self.__font.render(self.__text + ": "+ \
            str(self.__score), 1, self.__color)
        self.image = pygame.Surface((self.__width, self.__height))
        self.__W = self.__textSurf.get_width()
        self.__H = self.__textSurf.get_height()
        self.__drawText()

    def update(self, change = 0):
        self.image.fill(black)
        self.__score = change
        self.__textSurf = self.__font.render(self.__text + ": " + \
            str(self.__score), 1, self.__color)
        self.__drawText()

    def __drawText(self):
        self.rect = self.image.blit(self.__textSurf, (self.__width/2 - \
            self.__W/2, self.__height/2 - self.__H/2))
        pygame.display.update()

#----------------------------Text class end----------------------------------#

