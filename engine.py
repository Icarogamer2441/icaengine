import pygame as pg
from pygame.locals import *
from sys import exit

class ObjCircle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class ObjSquare:
    def __init__(self, x, y, width, height, color, border_radius):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.border_radius = border_radius
    
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

class Engine:
    def __init__(self, screensize, playerx, playery, gameversion, gamename):
        pg.init()
        self.objects = {}
        self.screensize = screensize
        self.screen = pg.display.set_mode(self.screensize)
        self.clock = pg.time.Clock()
        self.gamename = gamename
        self.screencolor = (0,0,0)
        self.functions = {}
        self.gameversion = gameversion
        pg.display.set_caption(f"{self.gamename} - {self.gameversion}")
        self.player_y = playerx
        self.player_x = playery
        self.player_vel = 5
        self.gravity = 0
        self.gravity_force = 1
    
    def run(self):
        while True:
            self.screen.fill(self.screencolor)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    exit()
            
            self.key = pg.key.get_pressed()
            
            for obj in self.objects:
                self.objects[obj].draw(self.screen)
            
            for function in self.functions:
                exec(self.functions[function])
            
            self.gravity += self.gravity_force

            self.clock.tick(60)

            pg.display.update()
    
    def PlayerMoveWASD(self):
        if self.key[K_w]:
            self.player_y -= self.player_vel
        elif self.key[K_s]:
            self.player_y += self.player_vel
        if self.key[K_a]:
            self.player_x -= self.player_vel
        elif self.key[K_d]:
            self.player_x += self.player_vel
    
    def PlayerMoveAD(self):
        if self.key[K_a]:
            self.player_x -= self.player_vel
        elif self.key[K_d]:
            self.player_x += self.player_vel
    
    def check_collision(self, rect1, rect2):
        return (rect1[0] < rect2[0] + rect2[2] and
                rect1[0] + rect1[2] > rect2[0] and
                rect1[1] < rect2[1] + rect2[3] and
                rect1[1] + rect1[3] > rect2[1])
