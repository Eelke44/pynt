import pygame as pg
from drawable import Drawable
from sound import Sound
from defaults import *


class Button(Drawable):
    def __init__(self, image: pg.Surface = None, color: tuple = (255,255,255), size = SMALL_BUTTON_SIZE, loc = (0,0), text = "", font = DEFAULT_FONT_LOC, fontSize = SMALL_FONT_SIZE, textFG = (0,0,0), border = SMALL_BUTTON_BORDER, onClick = lambda: None):
        super().__init__(size)
        if image:
            self.image = pg.transform.scale(image, size)
        else:
            self.image = None
        self.color = color
        self.text = text
        self.size = size
        self.loc = loc
        self.font = pg.font.Font(font, fontSize)
        self.textFG = textFG
        self.border = border
        self.onClick = onClick
        self.pressed = False
        self.hovered = False


    def updateState(self, event: pg.event.Event, game):
        onButton = self.mouseIsOnButton()
        if event.type == pg.MOUSEBUTTONDOWN and onButton:
            self.pressed = True
            game.playSound(Sound.HOVER)
            self.color = tuple(c/2 for c in self.color)
        elif event.type == pg.MOUSEBUTTONUP and self.pressed:
            if onButton:
                self.onClick()
            self.color = tuple(c*2 for c in self.color)
            self.pressed = False


    def mouseIsOnButton(self):
        x, y = pg.mouse.get_pos()
        left, top = self.loc
        right, bottom = (l+s for l, s in zip(self.loc, self.size))
        inWidth = left < x and x < right
        inHeight = top < y and y < bottom
        return inWidth and inHeight


    def draw(self, canvas: pg.Surface):
        textSurf = self.font.render(self.text, False, self.textFG)
        textRect = textSurf.get_rect()
        self.fill(self.color)
        if self.image:
            self.blit(self.image, (0,0))
        else:
            pg.draw.rect(self, tuple(c/2 for c in self.color), pg.Rect((0,0), self.size), width = self.border)
        w, h = self.size
        textRect.center = w//2, h//2
        self.blit(textSurf, textRect)
        canvas.blit(self, self.loc)


class QuitButton(Button):
    def __init__(self, loc = (0,0)):
        def onClick(): pg.event.post(pg.event.Event(pg.QUIT))
        super().__init__(text="Quit :(", color=(0,255,0), size=LARGE_BUTTON_SIZE, loc=loc, fontSize=LARGE_FONT_SIZE, onClick=onClick)


class PlayButton(Button):
    def __init__(self, game, text, loc = (0,0), size = LARGE_BUTTON_SIZE):
        def onClick(): game.setPlaying(True)
        super().__init__(text=text, color=(0,255,0), size=size, loc=loc, fontSize=LARGE_FONT_SIZE, onClick=onClick)


class ToMenuButton(Button):
    def __init__(self, loc = (0,0)):
        def onClick(): pg.event.post(pg.event.Event(TO_MENU_EVENT))
        super().__init__(text="To Menu", color=(0,255,0), size=LARGE_BUTTON_SIZE, loc=loc, fontSize=LARGE_FONT_SIZE, onClick=onClick)