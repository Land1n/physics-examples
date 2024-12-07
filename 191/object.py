import pygame as pg

class Object:
    def __init__(self,screen,image_path:str,pos:dict[int]=(0,0)):
        self.screen = screen
        self.image = pg.image.load(image_path)

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x  = pos[0]
        self.rect.y = pos[1]
    
    def move(self,x:int,y:int):
        self.rect.move_ip(x,y)

    def view(self):
        self.screen.blit(self.image,self.rect)

    @property
    def pos(self):
        return self.rect.x,self.rect.y

    @pos.setter
    def pos(self,pos:dict[int]):
        self.rect.x  = pos[0]
        self.rect.y = pos[1]

class Puck(Object):
    def __init__(self,screen,image_path:str,m:int,pos=(0,0)):
        super().__init__(screen,image_path,pos)


class Spring(Object):
    def __init__(self,screen,image_path:str,k:int,pos=(0,0)):
        super().__init__(screen,image_path,pos)


class SystemObects:
    def __init__(self,objs=[]) -> None:
        self.objs = objs

    