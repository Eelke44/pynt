import pygame as pg
from drawable import Drawable
from sound import *
from defaults import *


# Bottle cap
class Cap(Drawable):
    def __init__(self, loc, velocity, surfSize, rotSpeed, image):
        super().__init__(surfSize)
        self.loc = loc
        self.velocity = velocity
        self.size = surfSize
        self.rotSpeed = rotSpeed
        self.rotation = 0
        self.image = pg.transform.scale(image, (surfSize[0], surfSize[1]*14/31))
        self.blit(self.image, (0,0))


    def updateLoc(self, dt, game):
        self.loc = tuple(l + 0.001*dt*v for l, v in zip(self.loc, self.velocity))
        if self.loc[1] >= game.canvas.get_size()[1]:
            game.playSound(Sound.LAND)
            game.removeCap(self)
        self.rotation += self.rotSpeed*0.001*dt
        self.rotate(self.rotation)
    

    def updateVelocity(self, dt, acceleration):
        self.velocity = tuple(v + 0.001*dt*a for v, a in zip(self.velocity, acceleration))


    # Rotate relative to initial rotation
    def rotate(self, degs):
        self.fill(pg.Color(0,0,0,0))
        self.blit(pg.transform.rotate(self.image, degs), (0,0))


    def draw(self, canvas: pg.Surface):
        canvas.blit(self, self.loc)