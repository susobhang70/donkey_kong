from gameStatus import *

#----------------------------BoardLoader class-------------------------------#

class BoardLoader(gameStatus):
    """This class handles main initialization of the game"""

    def __init__(self):
        """Initializing the window"""
        #initialize pygame
        super().__init__()
        pygame.init()
        pygame.display.set_caption("Donkey Kong")
        #initializes screen and attributes
        self.__width = SCREEN_WIDTH
        self.__height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.__width, self.__height))
        self.__clock = pygame.time.Clock()

    def __wallLoader(self):
        """Loads the borders/walls of the window"""
        self.screen.fill(white)
        drawRect(self.screen, 0, 0, self.__width, self.__height, \
            black, SCREEN_THICK)

    def __levelLoader(self):
        """Loads the layout of the level"""
        self.__wallLoader()
        self._layoutDraw(self.screen)
        self._elementDraw(self.screen)
        self._collectCoin()
        self._updateText()

    def __winScreen(self):
        """This screen shows up when game is won after clearing all levels"""
        winText = pygame.font.SysFont("Arial",70)
        winSurf, winRect = text_objects("You Won! Press R to keep Playing", \
            winText)
        winRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
        self.screen.fill(white)
        self.screen.blit(winSurf, winRect)

        #During the white splash screen, player can either quit or continue
        #playing from level 1

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #window quit
                    sys.exit()
                elif event.type == KEYDOWN:
                    #quit by pressing q
                    if event.key == K_q:
                        sys.exit()
                    elif event.key == K_r:
                        #continue playing
                        self._level = 0          #back to level 0
                        return
            pygame.display.update()
            self.__clock.tick(15)

    def __winSplash(self):
        """This defines behavior of game after a level is won"""
        self._score += 50                        #50 points to rescue princess
        self._level += 1                         #increase level
        #if last level also cleared
        if self._level == 4:
            __winScreen(self.screen, self.__clock)
        #reset the gameElements and reload new level
        self._reset()
        self._coinLoader()

    def GameLoop(self):
        """Loop to keep the game running"""
        self._statusLoad()
        #timeElapsed tracks the elapsed time
        timeElapsed = [0, 0]
        while 1:
            timedelta = self.__clock.tick(FPS)
            for x in range(len(timeElapsed)):
                timeElapsed[x] += timedelta
            #load the level
            self.__levelLoader()
            #after certain inteval, change donkey's direction
            if timeElapsed[0] > DONKEY_DIRCHANGE:
                timeElapsed[0] = 0
                self._randomizeDonkey()
            #after certain intervals, spawn fireballs
            if timeElapsed[1] > FBALL_SPAWNTIME and \
            len(self._fireballList) < (4 * (self._level + 1)):
                timeElapsed[1] = 0
                for DonkeyKong in self._DonkeyList.sprites():
                    self._fireballLoader(DonkeyKong.getPosition(), \
                        DonkeyKong.getFloor())
            #quit the game
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or (event.type == KEYDOWN and \
                    event.key == K_q) or self._getLives() == 0):
                        sys.exit()
            #check if player collided
            if self._checkCollision() == 1:
                self._lostLife()
            #check if player won
            if self._Player.checkWin():
                self.__winSplash()

#----------------------------BoardLoader class end---------------------------#

#----------------------------Main game call----------------------------------#
if __name__ == "__main__":
    GameStart = BoardLoader()
    GameStart.GameLoop()
#----------------------------------------------------------------------------#
