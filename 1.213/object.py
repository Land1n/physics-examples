import pygame as pg

class Puck:
    def __init__(self, screen:pg.Surface, pos:dict[int] = (0,0),radius:int=30):
        self.screen = screen
        if pos == (0,0):
            self.pos = (radius,radius)
        else:
            self.pos = pos

        pg.draw.circle(self.screen,(0,0,0),self.pos,radius)
        pg.draw.circle(self.screen,(255,255,255),self.pos,0.9*radius)
        pg.draw.circle(self.screen,(0,0,0),self.pos,0.1*radius)


            