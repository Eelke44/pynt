import pygame as pg
from os import path
from binaryInsert import binaryInsert
from binaryRemove import binaryRemove
from sound import Sound
from barLocation import BarLoc
from drawable import Drawable
from bar import Bar
from bottle import Bottle
from menuBottle import MenuBottle
from cap import Cap
from buttons import *
from defaults import *
from util import *


class Pynt():
    def __init__(self):
        self.rand = init()
        self.canvas = createWindow()
        self.menuButtons: list[Button] = []
        self.gameEndedButtons: list[Button] = []
        self.bottles: dict[BarLoc, list[Bottle]] = {
            BarLoc.BAR: [],
            BarLoc.AIR: []
        }
        self.menuBottles: list[MenuBottle] = []
        self.trays = []
        self.caps: list[Cap] = []
        self.score = 0
        self.highScore = self.readHighScore()
        self.menuBeerSpawnRate = 10                         # Beers/second
        self.initMenuBottleSpeed = 60                       # Pixels/second
        self.initSlideSpeed = self.slideSpeed = 100         # Pixels/second of bottles sliding on the bar
        self.beerSlideSpeedInc = 5                          # Additional slide speed per second, updated once per beerIncInterval seconds
        self.initBeerSpawnRate = self.beerSpawnRate = 0.5   # Beers/second, updated once per beerIncInterval seconds
        self.beerSpawnRateInc = 0.1                         # Beers/second^2
        self.beerIncInterval = 2                            # Number of seconds in between increases in beer spawn rate and slide speed
        self.gravityAcc = (0,5000)                          # Acceleration of flying objects in pixels/second^2
        w, h = self.canvas.get_size()
        self.bottleSize = int(w*(68/1080)), int(h*(211/1920))
        self.capSurfSize = int(w*(31/1080)), int(h*(31/1920))
        self.sounds: dict[Sound, pg.mixer.Sound] = {
            Sound.LAND: [pg.mixer.Sound(path.join(AUDIO_LAND_PATH, f"land{i}.wav")) for i in range(1,9)],
            Sound.BOTTLE_SPAWN: [pg.mixer.Sound(path.join(AUDIO_BOTTLE_SPAWN_PATH, f"kling{i}.wav")) for i in range(1,9)],
            Sound.HOVER: [pg.mixer.Sound(path.join(AUDIO_BUTTON_PATH, "hover.wav"))],
            Sound.CLICK: [pg.mixer.Sound(path.join(AUDIO_BUTTON_PATH, "click.wav"))]
        }
        self.menuBG = pg.transform.scale(loadImage(MENU_BG_FILE), self.canvas.get_size())
        self.menuFG = pg.transform.scale(loadImage(MENU_FG_FILE), self.canvas.get_size())
        self.gameBG = pg.transform.scale(loadImage(GAME_BG_FILE), self.canvas.get_size())
        self.menuBottleImg = loadImage(MENU_BOTTLE_FILE)
        self.closedBottleImg = loadImage(CLOSED_BOTTLE_FILE)
        self.openedBottleImg = loadImage(OPENED_BOTTLE_FILE)
        self.capImg = loadImage(BOTTLE_CAP_FILE)


    # Main function
    def run(self):
        self.initButtonsAndDrawables()
        pg.time.set_timer(MENU_BEER_SPAWN_EVENT, int(1000/self.menuBeerSpawnRate))

        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        while self.running:
            self.handleEvents()
            if self.playing:    # In game
                self.drawGame()
                self.updateGamePhysics()
            else:               # Menu
                self.drawMenu()
                self.moveMenuBottles()
            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()


    def drawGame(self):
        self.canvas.blit(self.gameBG, (0, 0))
        for cap in self.caps:
            cap.draw(self.canvas)
        for surf in self.playingDrawables:
            surf.draw(self.canvas)
        for loc in self.bottles.values():
            for bottle in loc:
                bottle.draw(self.canvas)
        if self.gameEnded:  # Replay?
            for surf in self.gameEndedDrawables:
                surf.draw(self.canvas)
        self.drawHighScore()
        self.drawScore()
    

    def drawMenu(self):
        self.canvas.blit(self.menuBG, (0, 0))
        for bottle in self.menuBottles:
            bottle.draw(self.canvas)
        self.canvas.blit(self.menuFG, (0, 0))
        for surf in self.menuDrawables:
            surf.draw(self.canvas)
        self.drawMainText(TITLE, (0,0,0))


    def updateGamePhysics(self):
        self.slideBottles()
        self.moveCaps()


    # Handle the events of 1 game loop
    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == BEER_SPAWN_EVENT:
                self.spawnBottle(BarLoc.BAR)
            elif event.type == BEER_INC_EVENT:
                self.increaseBeerRates()
            elif event.type == TO_MENU_EVENT:
                self.toMenu()
            elif event.type == MENU_BEER_SPAWN_EVENT:
                self.spawnMenuBottle()
            elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                if self.playing:
                    if self.gameEnded:
                        for button in self.gameEndedButtons: button.updateState(event, self)
                    else:
                        for loc in self.bottles.values():
                            for bottle in loc: bottle.updateState(event)
                else:
                    for button in self.menuButtons: button.updateState(event, self)


    # Volume is a float between 0 and 1
    def playSound(self, sound: Sound):
        choice = self.rand.choice(self.sounds[sound])
        choice.play()


    def drawMainText(self, text, color):
        textSurf = pg.font.Font(DEFAULT_FONT_LOC, TITLE_FONT_SIZE).render(text, False, color)
        textRect = textSurf.get_rect()
        w, h = self.canvas.get_size()
        textRect.center = w//2, int(h*0.2)
        self.canvas.blit(textSurf, textRect)
    

    def initButtonsAndDrawables(self):
        self.genMenuButtons(self.canvas)
        self.genGameEndedButtons(self.canvas)
        self.menuDrawables: list[Drawable] = self.menuButtons
        self.playingDrawables: list[Drawable] = [Bar(self.canvas.get_size())]
        self.gameEndedDrawables: list[Drawable] = self.gameEndedButtons


    def drawScore(self):
        font = pg.font.Font(DEFAULT_FONT_LOC, TITLE_FONT_SIZE)
        scoreSurf = font.render(str(self.score), False, (255,255,255))
        scoreRect = scoreSurf.get_rect()
        w, h = self.canvas.get_size()
        scoreRect.center = w//2, int(h*0.15)
        self.canvas.blit(scoreSurf, scoreRect)


    def drawHighScore(self):
        font = pg.font.Font(DEFAULT_FONT_LOC, SMALL_FONT_SIZE)
        scoreSurf = font.render(f"High-score: {self.highScore}", False, (200,200,200))
        scoreRect = scoreSurf.get_rect()
        w = self.canvas.get_size()[0]
        margin = scoreRect.height//2
        scoreRect.topright = w - margin, margin
        self.canvas.blit(scoreSurf, scoreRect)


    def initBottles(self):
        self.bottles: dict[BarLoc, list[Bottle]] = {
            BarLoc.BAR: [],
            BarLoc.AIR: []
        }


    def gameOver(self):
        # Disable timers
        pg.time.set_timer(BEER_SPAWN_EVENT, 0)
        pg.time.set_timer(BEER_INC_EVENT, 0)
        self.gameEnded = True
        self.handleHighScore()
    

    def readHighScore(self):
        if not path.isfile(HIGH_SCORE_PATH): return 0
        with open(HIGH_SCORE_PATH, 'r') as highScoreFile:
            return int(highScoreFile.read())
    

    # Updates the high score if it was breached
    def handleHighScore(self):
        self.highScore = max(self.highScore, self.score)
        with open(HIGH_SCORE_PATH, 'w') as highScoreFile:
            highScoreFile.write(str(self.highScore))


    def slideBottles(self):
        for bottle in self.bottles[BarLoc.BAR]:
            bottle.move((-self.clock.get_time()/1000*bottle.slideSpeed,0))
    

    def moveCaps(self):
        for cap in self.caps:
            cap.updateLoc(dt(self), self)
            cap.updateVelocity(dt(self), self.gravityAcc)
    

    def moveMenuBottles(self):
        for bottle in self.menuBottles:
            bottle.updateLoc(dt(self), self)
            bottle.updateSpeed(dt(self), self.gravityAcc[1])


    def toMenu(self):
        self.setPlaying(False)


    # Start a new run of the game
    def setPlaying(self, playing):
        self.playing = playing
        if not playing:
            pg.time.set_timer(MENU_BEER_SPAWN_EVENT, int(1000/self.menuBeerSpawnRate))
            return
        self.gameEnded = False
        self.initBottles()
        self.score = 0
        self.beerSpawnRate = self.initBeerSpawnRate
        self.slideSpeed = self.initSlideSpeed
        self.spawnBottle(BarLoc.BAR)
        pg.time.set_timer(BEER_SPAWN_EVENT, int(1000/self.beerSpawnRate))
        pg.time.set_timer(BEER_INC_EVENT, int(1000*self.beerIncInterval))
        pg.time.set_timer(MENU_BEER_SPAWN_EVENT, 0)
            


    def genGameEndedButtons(self, canvas: pg.Surface):
        w, h = canvas.get_size()
        lbw, lbh = LARGE_BUTTON_SIZE
        playAgainButtonWidth = 350
        self.gameEndedButtons.append(PlayButton(self, "Play again!", ((w-playAgainButtonWidth)//2,(h-lbh)//2), (playAgainButtonWidth,100)))
        self.gameEndedButtons.append(ToMenuButton(((w-lbw)//2, int((h-lbh)//2 + 1.5*lbh))))

    # Add the menu buttons to the list
    def genMenuButtons(self, canvas: pg.Surface):
        w, h = canvas.get_size()
        lbw, lbh = LARGE_BUTTON_SIZE
        self.menuButtons.append(PlayButton(self, "Play!", ((w-lbw)//2,(h-lbh)//2)))
        self.menuButtons.append(QuitButton(((w-lbw)//2, int((h-lbh)//2 + 1.5*lbh))))
    

    # Called once every beerSpawnIncInterval seconds
    def increaseBeerRates(self):
        self.spawnBottle(BarLoc.BAR)
        self.beerSpawnRate += self.beerSpawnRateInc*self.beerIncInterval
        self.slideSpeed += self.beerSlideSpeedInc*self.beerIncInterval
        pg.time.set_timer(BEER_SPAWN_EVENT, int(1000/self.beerSpawnRate))    # Removes old beer spawn timer


    # Remove a bottle from the game (when it goes offscreen, called by the bottle)
    def removeBottle(self, bottle: Bottle):
        if not bottle.opened: self.gameOver()
        for loc in self.bottles.values():
            if binaryRemove(loc, bottle, lambda x: x.loc[1]):
                break
    

    def removeMenuBottle(self, bottle: MenuBottle):
        binaryRemove(self.menuBottles, bottle, lambda x: x.size[1])
    

    # Remove a cap from the game (when it goes offscreen, called by the cap)
    def removeCap(self, cap):
        self.caps.remove(cap)


    # Called when a bottle is opened (by the bottle itself)
    def bottleOpened(self, bottle, velocity):
        self.spawnCap(bottle, velocity)
        self.score += 1
    

    def spawnMenuBottle(self):
        w = self.canvas.get_size()[0]
        minScalar, maxScalar = 0.4, 0.6
        sizeScalar = self.rand.random()*(maxScalar - minScalar) + minScalar
        size = tuple(s*sizeScalar for s in self.canvas.get_size())
        bottle = MenuBottle(self.rand.randint(-self.canvas.get_size()[0] + 1, w), size, self)
        binaryInsert(self.menuBottles, bottle, lambda x: x.size[0])


    # Spawn a bottle at a given location in the bar
    def spawnBottle(self, loc: BarLoc):
        w, h = self.canvas.get_size()
        if loc == BarLoc.BAR:
            bottle = Bottle((w,h-self.rand.randint(int(0.405*h), int(0.491*h))), self.bottleSize, self)
            binaryInsert(self.bottles[BarLoc.BAR], bottle, lambda x: x.loc[1])


    # Called whenever a bottle is opened
    def spawnCap(self, bottle: Bottle, velocity):
        bX, bY = bottle.loc
        cX = bX + (bottle.size[0] - self.capSurfSize[0])//2
        cY = bY
        rotSpeed = self.rand.randint(360, 720)
        if self.rand.random() < 0.5: rotSpeed *= -1
        self.caps.append(Cap((cX, cY), velocity, self.capSurfSize, rotSpeed, self.capImg))


if __name__ == "__main__": Pynt().run()