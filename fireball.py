import random
from layout import *
from functions import *
from constants import *
#-----------------------------fireball class---------------------------------#

class fireball(pygame.sprite.Sprite, Layout):
    """Defines methods and attributes of fireball"""

    def __init__(self, x, y, level, floor):
        """Initializes fireball"""
        super().__init__()
        Layout.__init__(self)
        #set fireball length and breadth
        self.__w = FIREBALL_WIDTH
        self.__h = FIREBALL_HEIGHT
        #set fireball color
        self.__color = FIREBALL_COLOR
        #initialize fireball surface
        self.image = pygame.Surface([self.__w, self.__h])
        self.image.fill(self.__color)

        #set fireball level, color and speed
        self.__level = level
        self.__floor = floor
        #set fireball speed of movement
        self.__speed = FIREBALL_SPEED
        self.__air = 0                        #fireball in air or ladder status
        #fireball cords
        self.__x = x
        self.__y = y
        #select random initial direction of movement
        self.__chooseDirection()
        self.__drawFireball()

    def __drawFireball(self):
        """Function to draw the fireball object"""
        self.rect = drawRect(self.image, self.__x, self.__y, self.__w, \
            self.__h, self.__color)
        pygame.display.update(self.rect)

    def __resetFireball(self, x, floor):
        """Reset the fireball and spawn from donkey"""
        self.__x = x
        self.__y = self.redy[self.__level][floor] - self.__h
        self.__floor = floor
        self.__chooseDirection()

    def update(self, pos, floor):
        """updates the fireball position"""
        #extra parameters for spawning the fireball again if it reaches player
        #spawn position
        #adjust fireball with the floor if not falling
        if self.__air == 0:
            self.__y = self.redy[self.__level][self.__floor] - self.__h
        #if fireball is falling
        if self.__air == 1:
            #if fireball is about to hit the floor
            value = checkWall(self.__x, self.__y + 2 * (self.__speed), self.__w,\
             self.__h, wallyh = self.redy[self.__level][self.__floor])
            if value == 0:
                #adjust with the floor height
                if checkWall(self.__x, self.__y + (self.__speed), \
                    self.__w, self.__h, \
                    wallyh = self.redy[self.__level][self.__floor]) == 2:
                    self._moveDown()
                #end fall of the fireball
                self.__air = 0
                #choose random direction upon hitting floor
                self.__chooseDirection()
            else:
                #keep moving down if not hit floor
                self.__moveDown(2)

        #if fireball on last floor
        elif self.__floor == 5:
            if self.direction == "left":
                #if fireball hits player spawn position
                if checkWall(self.__x - 1, self.__y, self.__w, self.__h) == 3:
                    #reset the fireball
                    self.__resetFireball(pos, floor)
                else:
                    #keep moving left
                    self.__moveLeft()
            else:
                #if fireball hits right wall
                if checkWall(self.__x + self.__speed, self.__y, \
                    self.__w, self.__h) == 3:
                    #move the player to the left
                    self.__moveLeft()
                else:
                    #keep going right until it hits the wall
                    self.__moveRight()

        else:
            flag = 0
            #check if fireball is near a ladder to go down
            for i in range(len(self.bluex[self.__level])):
                if self.bluex[self.__level][i] == self.__x and \
                self.bluey[self.__level][i] - self.__h == self.__y:
                    #fireball is near ladder. Choose whether to go down
                    self.chooseDown()
                    flag = 1
                    break
            #if not near any ladder
            if flag == 0:
                self.move()
        self.__drawFireball()

    def __moveLeft(self, speedMultiplier = 1):
        """Make the fireball go left"""
        self.direction = "left"
        self.__x = self.__x - speedMultiplier * self.__speed

    def __moveRight(self, speedMultiplier = 1):
        """make the fireball go right"""
        self.direction = "right"
        self.__x = self.__x + speedMultiplier * self.__speed

    def __moveDown(self, speedMultiplier = 1):
        """make the fireball go down"""
        self.__y = self.__y + speedMultiplier * self.__speed

    def __chooseDirection(self):
        """Choose randomly whether to go left or right"""
        t = random.randint(0,1)
        if t == 0:
            self.direction = "left"
        else:
            self.direction = "right"

    def chooseDown(self):
        """Choose randomly whether to go down a ladder or keep going forward"""
        t = random.randint(0,1)
        if t == 0:
            #start going down
            self.__air = 1
            self.__moveDown(2)
            self.__floor = self.__floor + 1
        else:
            #keep moving forward
            self.move()

    def move(self):
        """Decisions regarding movement of the fireball"""
        if self.direction == "left":
            #check if the fireball can go further left
            xl = 0
            #check if the left boundary of floor is same as screen boundary.
            #If yes, then it cannot fall off
            if self.redx[self.__level][self.__floor] != WALLX_LOWER:
                xl = self.__w
            #check where fireball will be w.r.t. floor walls
            value = checkWall(self.__x - self.__speed, self.__y, self.__w, \
                self.__h, wallxl = self.redx[self.__level][self.__floor] - xl, \
                wallxh = self.redx[self.__level][self.__floor] + \
                self.redw[self.__level][self.__floor])
            #if going further left is possible
            if value == 1 :
                self.__moveLeft()
            #if fireball reached platform boundary
            elif value == 3 or value == 4:
                #fireball hit the screen boundary. So go other direction
                if xl == 0:
                    self.__moveRight()
                #fireball reached the end of platform and will fall off
                else:
                    self.__air = 1
                    self.__moveLeft()
                    self.__moveDown(2)
                    self.__floor = self.__floor + 1

        elif self.direction == "right":
            #check if fireball can go further right
            xh = 0
            #check if the left boundary of floor is same as screen boundary.
            #If yes, then it cannot fall off
            if self.redx[self.__level][self.__floor] + \
            self.redw[self.__level][self.__floor] != WALLX_HIGHER:
                xh = self.__w
            #check where fireball will be w.r.t. floor walls
            value = checkWall(self.__x + self.__speed, self.__y, self.__w, \
                self.__h, wallxl = self.redx[self.__level][self.__floor], \
                wallxh = self.redx[self.__level][self.__floor] + \
                self.redw[self.__level][self.__floor] + xh)
            #if going further right is possible
            if value == 1:
                self.__moveRight()
            #if fireball reached platform boundary
            elif value == 3 or value == 4:
                if xh == 0:
                    #fireball hit the screen boundary. So go other direction
                    self.__moveLeft()
                else:
                    #fireball reached the end of platform and will fall off
                    self.__air = 1
                    self.__moveRight()
                    self.__moveDown(2)
                    self.__floor = self.__floor + 1

#--------------------------fireball class end-------------------------------#
