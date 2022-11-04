import pygame as pg
from drawable import Drawable
from util import loadImage
from defaults import *


class Arch(Drawable):
    def __init__(self, size):
        super().__init__(size)
        self.size = size
        self.image = pg.transform.scale(loadImage(ARCH_FILE), size)
        self.blit(self.image, (0,0))


    def draw(self, canvas: pg.Surface):
        canvas.blit(self, (0,0))