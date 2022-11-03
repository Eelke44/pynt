import pygame as pg
from drawable import Drawable
from sound import Sound
from util import millis
from defaults import *


# Surface with a bottle. Bottle can be on a sub-surface and be open or closed.
# When bottle is opened, cap surface is spawned on main canvas to fall down.
class Bottle(Drawable):
    def __init__(self, loc, size, game, opened = False):
        super().__init__(size)
        self.loc = loc
        self.size = size
        self.game = game
        self.opened = opened
        self.slideSpeed = game.slideSpeed + game.rand.randint(-game.slideSpeed//3,game.slideSpeed//3)   # Fix this bottle's slidespeed
        self.hasEnteredScreen = False
        self.dragging = False   # True if user is dragging the cap off the bottle
        self.image = pg.transform.scale(game.openedBottleImg if opened else game.closedBottleImg, size)
        self.blit(self.image, (0,0))
        game.playSound(Sound.BOTTLE_SPAWN)
    

    def updateState(self, event: pg.event.Event):
        if self.opened: return
        if self.mouseIsAboveBottle():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.dragging = False
            elif self.dragging and event.type == pg.MOUSEBUTTONUP:
                self.open()
        elif self.mouseIsOnBottle():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.dragging = True
                self.dragStartLoc = pg.mouse.get_pos()
                self.dragStartTime = millis()
    

    def move(self, delta):
        onScreen = self.isOnScreen()
        if not self.hasEnteredScreen and onScreen: self.hasEnteredScreen = True
        self.loc = tuple(val + deltaVal for val, deltaVal in zip(self.loc, delta))
        if self.hasEnteredScreen and not onScreen: self.game.removeBottle(self)

    def open(self):
        self.fill(pg.Color(0,0,0,0))
        self.opened = True
        self.blit(pg.transform.scale(self.game.openedBottleImg, self.size), (0,0))
        distance = (pEnd - pStart for pEnd, pStart in zip(pg.mouse.get_pos(), self.dragStartLoc))
        deltaTime = millis() - self.dragStartTime
        self.game.bottleOpened(self, tuple(1000*d/deltaTime for d in distance))
    

    def isOnScreen(self):
        w, h = self.game.canvas.get_size()
        x, y = self.loc
        bW, bH = self.size
        isInWidth = 0 < x + bW and w > x
        isInHeight = 0 < y + bH and h > y
        return isInWidth and isInHeight


    def mouseIsAboveBottle(self):
        y = pg.mouse.get_pos()[1]
        top = self.loc[1]
        return y < top


    def mouseIsOnBottle(self):
        x, y = pg.mouse.get_pos()
        left, top = self.loc
        right, bottom = (l+s for l, s in zip(self.loc, self.size))
        inWidth = left < x and x < right
        inHeight = top < y and y < bottom
        return inWidth and inHeight


    def draw(self, canvas: pg.Surface):
        canvas.blit(self, self.loc)