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

class Game:
    def __init__(self, screensize, playerx, playery, gameversion, gamename):
        pg.init()
        self.variables = {"points": 0}
        self.events = {"OnGameStart": "",
        "OnPlayerWalk": "",
        "OnGameEnd": "",
        "OnGameRunning": "",
        "OnGameStartAndEnd": ""}
        self.screensize = screensize
        self.screen = pg.display.set_mode(self.screensize)
        self.clock = pg.time.Clock()
        self.gamename = gamename
        self.screencolor = (0,0,0)
        self.scripts = {}
        self.filescripts = []
        self.gameversion = gameversion
        pg.display.set_caption(f"{self.gamename} - {self.gameversion}")
        self.player_y = playerx
        self.player_x = playery
        self.player_vel = 5
        self.gravity = 0
        self.gravity_force = 1
        self.objects = {}
    
    def Start(self):
        exec(self.events.get("OnGameStart"))
        exec(self.events.get("OnGameStartAndEnd"))
        while True:
            self.screen.fill(self.screencolor)
            for event in pg.event.get():
                if event.type == QUIT:
                    exec(self.events.get("OnGameEnd"))
                    exec(self.events.get("OnGameStartAndEnd"))
                    pg.quit()
                    exit()
            
            self.key = pg.key.get_pressed()

            for obj in self.objects:
                self.objects[obj].draw(self.screen)
            
            for script in self.scripts:
                exec(self.scripts[script])
            
            for filename in self.filescripts:
                with open(filename + ".icaeng", "r") as f:
                    content = f.read()
                exec(content)
            
            exec(self.events.get("OnGameRunning"))
            
            self.gravity += self.gravity_force

            self.clock.tick(60)

            pg.display.update()
    
    def PlayerMoveWASD(self):
        if self.key[K_w]:
            exec(self.events.get("OnPlayerWalk"))
            self.player_y -= self.player_vel
        elif self.key[K_s]:
            exec(self.events.get("OnPlayerWalk"))
            self.player_y += self.player_vel
        if self.key[K_a]:
            exec(self.events.get("OnPlayerWalk"))
            self.player_x -= self.player_vel
        elif self.key[K_d]:
            exec(self.events.get("OnPlayerWalk"))
            self.player_x += self.player_vel

    
    def PlayerMoveAD(self):
        if self.key[K_a]:
            exec(self.events.get("OnPlayerWalk"))
            self.player_x -= self.player_vel
        elif self.key[K_d]:
            exec(self.events.get("OnPlayerWalk"))
            self.player_x += self.player_vel
    
    def check_collision(self, rect1, rect2):
        return (rect1[0] < rect2[0] + rect2[2] and
                rect1[0] + rect1[2] > rect2[0] and
                rect1[1] < rect2[1] + rect2[3] and
                rect1[1] + rect1[3] > rect2[1])

    def change_points(self, add, remove):
        self.variables["points"] += add
        self.variables["points"] -= remove
    
    def collision_box(self, x,y,sizex,sizey):
        return pg.Rect(x,y,sizex,sizey)
