import os
import sys
import time
import random
import pygame
from pygame.locals import *
from constants import *
from functions import *
from layout import *
from person import *
from donkey import *
from player import *
from fireball import *
from coinText import *

#------------------------Game Elements class--------------------------------#
class gameElements(Layout):
    """This class initializes and defines methods for game elements"""

    def __init__(self):
        """Initialize level and all groups of sprites"""
        super().__init__()
        self._fireballList = pygame.sprite.Group()
        self._DonkeyList = pygame.sprite.Group()
        self._playerList = pygame.sprite.Group()
        self._coinList = pygame.sprite.Group()
        self._princessList = pygame.sprite.Group()
        self._textList = pygame.sprite.Group()
        self._level = START_LEVEL

    def __princessLoader(self):
        """Loads the princess object"""
        princess = person(self.princessx[self._level], \
            self.princessy[self._level], pink)
        self._princessList.add(princess)

    def _coinLoader(self):
        """Loads all coins for a level"""
        #kills existing coins first
        for coin in self._coinList.sprites():
            coin.kill()
        for i in range(MAX_COINS):
            newcoin = coins(self._level)
            self._coinList.add(newcoin)

    def _fireballLoader(self, xy, floor):
        """Loads fireballs from a donkey"""
        ball = fireball(xy[0] + xy[2] + 1, xy[1], self._level, floor)
        self._fireballList.add(ball)

    def __donkeyLoader(self):
        """Loads donkies on the screen according to level"""
        for i in range(self._level + 1):
            DonkeyKong = donkey(self.donkeyx[self._level][i], \
                self.donkeyy[self._level][i], self._level, i+1)
            self._DonkeyList.add(DonkeyKong)

    def _layoutDraw(self, screen):
        """Draws the whole layout of the level"""
        #Draws Cage
        drawRect(screen, self.cagex[self._level], \
            self.cagey[self._level], self.cagew[self._level], \
            self.cageh[self._level], grey, CAGE_THICK)
        #Draws Red Platforms
        for i in range(len(self.redx[self._level]) - 1):
            drawRect(screen, self.redx[self._level][i], \
                self.redy[self._level][i], self.redw[self._level][i], \
                self.redh[self._level][i], red)
        #Draws Blue Ladders
        for i in range(len(self.bluex[self._level])):
            drawRect(screen, self.bluex[self._level][i], \
                self.bluey[self._level][i], self.bluew[self._level][i], \
                self.blueh[self._level][i], blue)
        #Draws Blue broken Ladders
        for i in range(len(self.bluebrokenx[self._level])):
            drawRect(screen, \
                self.bluebrokenx[self._level][i], \
                self.bluebrokeny[self._level][i] + \
                self.bluebrokenh[self._level][i], \
                self.bluebrokenw[self._level][i], \
                self.bluebrokenh[self._level][i], \
                white)

    def __playerLoader(self):
        """Loads the player"""
        self._Player = player(self._level)
        self._playerList.add(self._Player)

    def __updateCoin(self):
        """updates all the coins"""
        self._coinList.update()

    def __updateDonkey(self):
        """updates the donkey on the screen"""
        self._DonkeyList.update()

    def _randomizeDonkey(self):
        """randomizes the movement of all donkies on the screen"""
        for DonkeyKong in self._DonkeyList.sprites():
            DonkeyKong.randomDirection()

    def __updateFireball(self):
        """updates the movement of fireball"""
        #selecting a random donkey for spawning of fireball if it reaches
        #player spawn position
        x = random.randint(0, len(self._DonkeyList) - 1)
        i = 0
        for DonkeyKong in self._DonkeyList.sprites():
            if i == x:
                self._fireballList.update(DonkeyKong.getXCord(), \
                    DonkeyKong.getFloor())
                return
            i += 1

    def __updatePrincess(self):
        """updates the princess object"""
        self._princessList.update()

    def __updatePlayer(self):
        """updates the player object"""
        self._playerList.update()

    def __playerMove(self):
        """defines the movement of the player according to the key pressed"""
        keypress = pygame.key.get_pressed()
        #if the player is still in a jump
        if self._Player.checkJump():
            self._Player.jumpUp()
        if keypress[K_SPACE]:
            if self._Player.checkJump() or self._Player.checkAir() \
            or self._Player.checkLadder():
                #player is already in a jump, freefall or ladder
                pass
            else:
                self._Player.jumpUp()
        if keypress[K_d]:
            self._Player.moveRight()
        elif keypress[K_a]:
            self._Player.moveLeft()
        else:
            #ladder movements
            if self._Player.checkJump() or self._Player.checkAir():
                pass
            elif keypress[K_s]:
                self._Player.ladderDown()
            elif keypress[K_w]:
                self._Player.ladderUp()

    def _checkCollision(self):
        """Returns true if the player has collided with a fireball or donkey
            and resets the level, else returns false"""
        #checking if hit by fireball
        blocks_hit_list = pygame.sprite.spritecollide(self._Player, \
            self._fireballList, False)
        if len(blocks_hit_list) != 0:
            return 1
        #checking if hit by a donkey
        donkey_hit = pygame.sprite.spritecollide(self._Player, \
            self._DonkeyList, False)
        if len(donkey_hit) != 0:
            return 1
        #no hit occured
        return 0

    def _resetElements(self):
        """reset the game Elements except coins"""
        #kills game elements
        self._Player.kill()
        for donkeyObject in self._DonkeyList.sprites():
            donkeyObject.kill()
        for princess in self._princessList.sprites():
            princess.kill()
        for fBall in self._fireballList.sprites():
            fBall.kill()
        #loads the game elements afresh
        self.__donkeyLoader()
        self.__playerLoader()
        self.__princessLoader()

    def _elementDraw(self, screen):
        """Draws all elements on the screen and updates according to player
         movement"""
        self._playerList.draw(screen)
        self._coinList.draw(screen)
        self._fireballList.draw(screen)
        self._DonkeyList.draw(screen)
        self._textList.draw(screen)
        self._princessList.draw(screen)
        self.__playerMove()
        self.__elemUpdate()

    def _elemLoader(self):
        """Loads all the game Element objects"""
        self.__donkeyLoader()
        self.__playerLoader()
        self._coinLoader()
        self.__princessLoader()

    def __elemUpdate(self):
        """updates all the game Elements"""
        self.__updateDonkey()
        self.__updateFireball()
        self.__updatePlayer()
        self.__updateCoin()
        self.__updatePrincess()

#----------------------------GameElements class end--------------------------#
