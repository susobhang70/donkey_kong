from gameElements import *

class gameStatus(gameElements):
    """Handles game status variables and methods"""
    def __init__(self):
        super().__init__()
        #game status variables
        self._lives = PLAYER_LIVES
        self._score = 0

    def _getLives(self):
        """returns lives of the player"""
        return self._lives

    def _lostLife(self):
        """changes status of game when player dies"""
        self._lives -= 1
        self._score -= 25
        self._reset()

    def _reset(self):
        """resets the whole game"""
        self.__showScore.update(self._score)
        self.__showLife.update(self._lives)
        self._resetElements()

    def _updateText(self):
        """Update all the text status messages"""
        self.__showScore.update(self._score)
        self.__showLevel.update(self._level + 1)
        self.__showLife.update(self._lives)

    def __lifeShow(self):
        """Shows status of player's lives"""
        self.__showLife = Text(text = "Lives", score = self._lives, \
            width = LIVES_X, height = LIVES_Y)
        self._textList.add(self.__showLife)

    def __scoreLoader(self):
        """Shows the score of the player"""
        self.__showScore = Text(score = self._score, text = "Score", \
            width = SCORE_X, height = SCORE_Y)
        self._textList.add(self.__showScore)

    def __levelShow(self):
        """Shows the game level"""
        self.__showLevel = Text(text = "Level", score = self._level + 1,\
         width = LEVEL_X, height = LEVEL_Y)
        self._textList.add(self.__showLevel)

    def _statusLoad(self):
        """Loads all status elements with game Elements"""
        self._elemLoader()
        self.__levelShow()
        self.__scoreLoader()
        self.__lifeShow()

    def _collectCoin(self):
        """updates score upon collection of coin"""
        coinHit = pygame.sprite.spritecollide(self._Player, \
            self._coinList, True)
        self._score += (5 * len(coinHit))
