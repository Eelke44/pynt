import pygame as pg

class Drawable(pg.Surface):
    def __init__(self, size):
        super().__init__(size, pg.SRCALPHA)

    def draw(self, canvas: pg.Surface):
        pass