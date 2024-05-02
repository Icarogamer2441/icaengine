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

class ObjTriangle:
        def __init__(self, x1, y1, x2, y2, x3, y3, color):
            self.points = [(x1, y1), (x2, y2), (x3, y3)]
            self.color = color
        
        def draw(self, screen):
            pg.draw.polygon(screen, self.color, self.points)

class ObjLine:
        def __init__(self, x1, y1, x2, y2, width, color):
            self.start = (x1, y1)
            self.end = (x2, y2)
            self.width = width
            self.color = color
        
        def draw(self, screen):
            pg.draw.line(screen, self.color, self.start, self.end, self.width)

class Game:
    def __init__(self, screensize, playerx, playery, gameversion, gamename):
        pg.init()
        self.variables = {"points": 0}
        self.events = {"OnGameStart": "",
        "OnPlayerWalk": "",
        "OnGameEnd": "",
        "OnGameRunning": "",
        "OnGameStartAndEnd": "",
        "OnMouseClick": "",
        "OnMouseHover": ""}
        self.texts = {}
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
                self.event = event
                if  event.type == QUIT:
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
            
            for text in self.texts:
                textvalue = self.texts.get(text)
                if textvalue.startswith("self.create_text"):
                    exec(textvalue)
                else:
                    print(f"inavlid script to create text on text: {text}. with code: {textvalue}")
            
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

    def change_background_color(self, new_color):
        self.screencolor = new_color
    
    def play_sound(self, sound_file):
        sound = pg.mixer.Sound(sound_file)
        sound.play()

    def on_mouse_click(self):
        if self.event.type == MOUSEBUTTONDOWN:
            if BUTTON_LEFT:
                return True
            else:
                return False

    def on_mouse_hover(self, x, y, width, height):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if x < mouse_x < x + width and y < mouse_y < y + height:
            return True
        else:
            return False
        
    def create_text(self, text, font_size, font_color, x, y, font_name=None):
        font = pg.font.Font(font_name, font_size) if font_name else pg.font.Font(None, font_size)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
