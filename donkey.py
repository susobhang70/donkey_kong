import random
from layout import *
from person import *
from functions import *
#---------------------------Donkey Class-------------------------------------#

class donkey(person, Layout):
    """Class for donkey kong's methods"""

    def __init__(self, x, y, level, floor, color = brown):
        """Initializes donkey and its movement limits"""
        super().__init__(x, y, color, level + 1)
        Layout.__init__(self)
        #spawning floor of donkey
        self.__floor = floor
        #current level
        self.__level = level

    def update(self):
        """specifies movement of donkey"""
        if self._getDirection() == "right":
            #if hits right boundary of platform
            if self._x >= self.redx[self.__level][self.__floor] + \
            self.redw[self.__level][self.__floor] - self._w - self._speed:
                self._moveLeft()
            else:                                        #move right
                self._moveRight()

        elif self._getDirection() == "left":
            #if hits left boundary of platform
            if self._x <= self.redx[self.__level][self.__floor] + self._speed:
                self._moveRight()
            else:                                        #move left
                self._moveLeft()
        self._drawPerson()

    def randomDirection(self):
        """selects a random direction for donkey"""
        t = random.randint(0,1)
        if t == 1:
            self.changeDirection("left")
        else:
            self.changeDirection("right")

    def getFloor(self):
        """returns the floor number of the donkey"""
        return self.__floor

    def getXCord(self):
        """returns the x co-ordinate of the donkey"""
        return self._x

#--------------------------donkey Class End----------------------------------#
