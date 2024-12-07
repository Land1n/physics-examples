import pygame as pg
import sys

import math

from object import Puck

def run(N,VA=1):
    pg.init()

    screen = pg.display.set_mode((500,300))
    pg.display.set_caption("Задача: 1.213")
    clock = pg.time.Clock()
    startExperiment = False

    time1 = 0
    time2 = 0

    x0A = 250-N 
    xA = x0A
    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    startExperiment = True if not startExperiment else False
                    xA = x0A
                    time1 = 0
                    time2 = 0
                    Puck(screen,(xA,150))

        screen.fill((255,255,255))


        if startExperiment:
            if xA < 250:
                time1 += 1
                xA  = VA*time1 + x0A
                Puck(screen,(xA,150))
                Puck(screen,(300,120))
                Puck(screen,(300,180))
                
            if round(xA) == 250:
                time2 += 1
                A = (250 + VA*time2*((250-N)**2-2)/(6-(250-N)**2),150)
                B = (300+VA*time2*math.sin(math.sqrt(50**2+30**2)/50),120-VA*time2*math.sin(math.sqrt(50**2+30**2)/50))
                C = (300+VA*time2*math.sin(math.sqrt(50**2+30**2)/50),180+VA*time2*math.sin(math.sqrt(50**2+30**2)/50))
                Puck(screen,A)
                Puck(screen,C)
                Puck(screen,B)
                
        else:
            Puck(screen,(xA,150))
            Puck(screen,(300,120))
            Puck(screen,(300,180))
        
        pg.display.flip()
        clock.tick(300)
if __name__ == "__main__":
    n1 = 248
    n2 = 250-math.sqrt(2)
    n3 = 250
    run(n1,VA=1)