import pygame as pg
from drawable import Drawable
from sound import Sound
from util import millis
from defaults import *


# Surface with a bottle. Bottle can be on a sub-surface and be open or closed.
# When bottle is opened, cap surface is spawned on main canvas to fall down.
class MenuBottle(Drawable):
    def __init__(self, xPos, size, game):
        super().__init__(size)
        self.loc = (xPos, -size[1])
        self.size = size
        self.game = game
        self.speed = game.initMenuBottleSpeed + game.rand.randint(-game.initMenuBottleSpeed//3,game.initMenuBottleSpeed//3)
        self.image = pg.transform.scale(game.menuBottleImg, size)
        self.blit(self.image, (0,0))
    

    def updateLoc(self, dt, game):
        self.loc = (self.loc[0], self.loc[1] + self.speed*0.001*dt)
        if self.loc[1] >= game.canvas.get_size()[1]:
            game.removeMenuBottle(self)
    

    def updateSpeed(self, dt, acceleration):
        self.speed += acceleration*0.001*dt


    def draw(self, canvas: pg.Surface):
        canvas.blit(self, self.loc)