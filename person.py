import pygame
from functions import *
from pygame.locals import *
from constants import *

#--------------------------Person Class--------------------------------------#

class person(pygame.sprite.Sprite):
    """Class for person in game and movement methods"""

    def __init__(self, x, y, color, speed = 0, direction = "right"):
        """Initialize a person with color, direction, position and image"""
        super().__init__()
        self._direction = direction                      #set default direction
        self._speed = speed                              #set default speed
        #person spawn coordinates
        self._x, self._y = x, y
        #person dimensions and color
        self._w, self._h = PERSON_WIDTH, PERSON_HEIGHT
        self._color = color
        #person image
        self.image = pygame.Surface([self._w, self._h])
        self.image.fill(color)
        self._drawPerson()

    def _drawPerson(self):
        """function to draw the person object"""
        self.rect = drawRect(self.image, self._x, self._y, self._w, self._h, \
            self._color)
        pygame.display.update()

    def changeDirection(self, direction):
        """change movement direction of object"""
        self._direction = direction

    def update(self):
        """to redraw the person object again"""
        self._drawPerson()

    def getPosition(self):
        """returns position of the person"""
        xy=[self._x, self._y, self._w, self._h]
        return xy

    def _getDirection(self):
        """returns movement direction"""
        return self._direction

    def _moveLeft(self):
        """moves person towards left"""
        self.changeDirection("left")
        self._x = self._x - self._speed

    def _moveRight(self):
        """moves person towards right"""
        self.changeDirection("right")
        self._x = self._x + self._speed

    def _moveUp(self, speed = None):
        """moves person upwards"""
        if speed == None:
            speed = self._speed
        self._y = self._y - speed

    def _moveDown(self, speed = None):
        """moves person downwards"""
        if speed == None:
            speed = self._speed
        self._y = self._y + speed

#---------------------------Person Class end---------------------------------#
