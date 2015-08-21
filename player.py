from person import *
from layout import *

#--------------------------player Class--------------------------------------#

class player(person, Layout):
    """Class for player methods"""

    def __init__(self, level, x = WALLX_LOWER, y = WALLY_HIGHER - 20, \
        speed = 2, color = green):
        """Initializes player"""
        person.__init__(self, x, y, color, speed)
        Layout.__init__(self)
        self.__level = level
        self.__floor = 5                         #player always on last floor
        self.__ladder = 0                        #bool for player on ladder
        self.__jump = 0                          #player jump stage
        self.__air = 0                           #player in freefall status

    def update(self):
        """updates the player object and redraws"""
        self.__airCheck()
        self._drawPerson()

    def __airCheck(self):
        """Checks if player is in the air and continues the freefall.
            This is NOT a function for checking jump"""
        if self.__air == 1:
            value = checkWall(self._x, self._y + self._speed, self._w,\
             self._h, wallyh = self.redy[self.__level][self.__floor])
            #if player about to hit floor
            if value == 0:
                #reduce fall size to bring to level platform
                if checkWall(self._x, self._y + (self._speed / 2), self._w, \
                    self._h, wallyh = self.redy[self.__level][self.__floor]) \
                    == 2:
                    self._moveDown(1)
                self.__air = 0
            else:                               #continue moving down
                self._moveDown()

    def moveLeft(self):
        """Move the player to the left"""
        #check if the player is not on ladder and going left is possible or not
        if self.__ladder != 1 and checkWall(self._x - self._speed, self._y, \
            self._w, self._h) != 0 :
            self._x = self._x - self._speed

        #check if the player is about to fall off the platform going left
        xl = 0
        #if the platform left boundary is same as screen left boundary
        if self.redx[self.__level][self.__floor] != WALLX_LOWER:
            xl = self._w
        #check for freefall
        value = checkWall(self._x, self._y, self._w, self._h, \
            wallxl = self.redx[self.__level][self.__floor] - xl, wallxh = \
            self.redx[self.__level][self.__floor] + \
            self.redw[self.__level][self.__floor])
        if value == 3 or value == 4:
            if xl != 0:
                self.__air = 1                          #freefall initiated
                self.__floor += 1

    def moveRight(self):
        """Move the player to the right"""
        #check if player is not on ladder and going right is possible or not
        if self.__ladder != 1 and checkWall(self._x + self._speed, self._y, \
            self._w, self._h) != 0 :
            self._x = self._x + self._speed

        #check if the player is about to fall off the platform going right
        xh = 0
        #if the platform is same as the screen right boundary
        if self.redx[self.__level][self.__floor] + \
        self.redw[self.__level][self.__floor] != WALLX_HIGHER:
            xh = self._w
        #check for freefall
        value = checkWall(self._x, self._y, self._w, self._h, \
            wallxl = self.redx[self.__level][self.__floor], wallxh = \
            self.redx[self.__level][self.__floor] + \
            self.redw[self.__level][self.__floor] + xh)
        if value == 3 or value == 4:
            if xh != 0:
                self.__air = 1                          #freefall initiated
                self.__floor += 1

    def ladderUp(self):
        """Move the player up the ladder"""
        #check if the player is on the floor of the princess
        if  self.__floor == 0 and \
            self._y == self.redx[self.__level][self.__floor] - self._h:
            return

        #if the ladder movement upwards has not been initiated
        elif self.__ladder == 0:
            #check all ladders
            for i in range(len(self.bluex[self.__level])):
                #checking if player is near a ladder to climb up
                if self._x >= self.bluex[self.__level][i] - XOFFSET and \
                self._x <= self.bluex[self.__level][i] + self._w + XOFFSET and\
                 self._y == self.bluey[self.__level][i] + \
                self.blueh[self.__level][i] - self._h:
                    #check if the player is trying to climb a broken ladder
                    for j in range(len(self.bluebrokenx[self.__level])):
                        if self.bluex[self.__level][i] == \
                        self.bluebrokenx[self.__level][j] \
                        and self.bluey[self.__level][i] == \
                        self.bluebrokeny[self.__level][j]:
                            #broken ladder cannot climb
                            return
                    #ladder is not broken. Initiate climb
                    self.__ladder = 1
                    self._x = self.bluex[self.__level][i]
                    self._moveUp()
                    #store the ladder number
                    self.ladderNumber = i
                    #floor points to the upper floor of the ladder
                    self.__floor -= 1
                    break

        #if player is already on ladder
        elif self.__ladder == 1:
            #if the player is about to reach the upper floor
            if self._y - self._speed <= \
            self.bluey[self.__level][self.ladderNumber] - self._h:
                if self._y - self._speed < \
                self.bluey[self.__level][self.ladderNumber] - self._h:
                    #to adjust player with floor
                    self._moveUp(self._speed / 2)
                else:
                    self._moveUp()
                #player no longer on a ladder
                self.__ladder = 0
            #keep climbing if not near upper floor
            else:
                self._moveUp()

    def ladderDown(self):
        """Move the player down the ladder"""
        #No ladder down on the last floor
        if self.__floor == 5:
            return

        #If player is not already on the ladder
        elif self.__ladder == 0:
            #check all ladders
            for i in range(len(self.bluex[self.__level])):
                #check if player is near any ladder to climb down
                if self._x >= self.bluex[self.__level][i] - XOFFSET and \
                self._x <= self.bluex[self.__level][i] + self._w + XOFFSET and\
                 self._y == self.bluey[self.__level][i] - self._h:
                    #check if the player is trying to climb a broken ladder
                    for j in range(len(self.bluebrokenx[self.__level])):
                        if self.bluex[self.__level][i] == \
                        self.bluebrokenx[self.__level][j] \
                        and self.bluey[self.__level][i] == \
                        self.bluebrokeny[self.__level][j]:
                            #broken ladder cannot climb
                            return
                    #ladder not broken. Climb down initiated
                    self.__ladder = 1
                    self._x = self.bluex[self.__level][i]
                    self._moveDown()
                    #store the ladder number
                    self.ladderNumber = i
                    break

        #if the player is already on the ladder
        elif self.__ladder == 1:
            #if the player is about to reach the lower floor
            if self._y + self._speed + self._h >= \
            self.bluey[self.__level][self.ladderNumber] + \
            self.blueh[self.__level][self.ladderNumber] :
                if self._y + self._speed + self._h > \
                self.bluey[self.__level][self.ladderNumber] + \
                self.blueh[self.__level][self.ladderNumber] :
                    #adjust player with lower floor
                    self._moveDown(self._speed / 2)
                else:
                    self._moveDown()
                #stop ladder movement and increase floor
                self.__ladder = 0
                self.__floor += 1

            else:
                #keep climbing down if not near lower floor
                self._moveDown()

    def checkLadder(self):
        """Returns true if player is on the ladder"""
        return self.__ladder

    def checkAir(self):
        """Returns true if the player is in freefall"""
        return self.__air

    def checkJump(self):
        """Returns true if the player is in the middle of a jump"""
        if self.__jump == 0:
            return 0
        else:
            return 1

    def checkWin(self):
        """check if the player has won the level"""
        #if player on last floor and is on same height with princess
        if self.__floor == 0 and self._y == self.princessy[self.__level]:
            return 1
        else:
            return 0

    def jumpUp(self):
        """make the player jump up"""
        self.__jump += 1
        #keep on rising up the player
        if self.__jump <= 29:
            self._y = self._y - self._speed
        #falling down part of the jump
        elif self.__jump > 29 and self.__jump <= 58:
            self._y = self._y + self._speed
            #player reached the floor, end jump
            if self.__jump == 58:
                self.__jump = 0
#------------------------player class end------------------------------------#
