import pygame as pg
from os import path
from random import Random
from defaults import *


def init(seed = RANDOM_SEED):
    pg.init()
    return Random(seed)


def loadImage(name):
    return pg.image.load(path.join(IMG_DIR, name)).convert_alpha()


def createWindow():
    pg.display.set_caption(WINDOW_CAPTION)
    info = pg.display.Info()
    height = int(info.current_h*0.8)
    width = height*9//16
    return pg.display.set_mode((width, height))


# Time since pygame.init()
def millis():
    return pg.time.get_ticks()


def dt(game):
    return game.clock.get_time()