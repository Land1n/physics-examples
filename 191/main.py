import pygame as pg
import sys
import math

from object import Puck,Spring,Object


def run(m1:int,m2:int,k:int,x:int):
    pg.init()
    screen = pg.display.set_mode((500,300))
    pg.display.set_caption("Задача: 191")
    bg_color = (255,255,255)
    time = pg.time
    clock = pg.time.Clock()
    objs = {
        "puck1" : Puck(
            screen=screen,
            image_path="191\image\шайба.png",
            pos=(10,190),
            m=m1
        ),
        "puck2" : Puck(
            screen=screen,
            image_path="191\image\шайба.png",
            m=m2,
            pos=(210,190)
        ),
        "spring":Spring(screen,f"191\image\пружина0.png",k,pos=(110,190)),
        "wall_bottom" : Object(
            screen=screen,
            image_path="191\image\стена_низ.png",
            pos=(0,290),
        ),
        "wall_left" : Object(screen,"191\image\стена_лево.png") ,
    }
    i = 0
    step1 = True
    step2 = False
    step3 = False
    pos_x_spring = 110

    startExperiment = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    startExperiment = True if not startExperiment else False
                    objs["puck2"].pos=(210,190)
                    objs["puck1"].pos=(10,190)
                    i = 0
                    j = 10
                    pos_x_spring = 110
                    objs["spring"] = Spring(screen,f"191\image\пружина{i}.png",k,pos=(110,190))
                    step1 = True
                    step2 = False
                    step3 = False
        screen.fill(bg_color)
        for obj in objs.values():
            obj.view()
        pg.display.flip()
        if startExperiment:
            if i == 11:
                step1 = False
                step2 = False
                step3 = False
                print("пружинка порвалась")
                startExperiment = False
            if step1:
                i += 1
                if i < x//10:
                    objs["puck2"].move(10,0)
                    objs["spring"] = Spring(screen,f"191\image\пружина{i}.png",k,pos=(pos_x_spring,190))
                    time.wait(10)
                else: 
                    step1 = False
                    step2 = True
                pg.display.flip()
            if step2:
                i -= 1
                if i > 0:
                    pos_x_spring += 10
                    objs["puck1"].move(10,0)
                    objs["spring"] = Spring(screen,f"191\image\пружина{i}.png",k,pos=(pos_x_spring,190))
                    time.wait(10)
                else: 
                    objs["puck2"].move(10,0)
                    step2 = False
                    step3 = True
                pg.display.flip()
            if step3:
                objs["puck1"].move(((x*math.sqrt(m2*k))//(m1+m2)),0)
                objs["puck2"].move(((x*math.sqrt(m2*k))//(m1+m2)),0)
                objs["spring"].move(((x*math.sqrt(m2*k))//(m1+m2)),0)
                pg.display.flip()
        
        clock.tick(30)
if __name__ == "__main__":
    run(1000,200,10,100)