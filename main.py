from engine import *
import pygame as pg
from pygame.locals import *
from sys import exit

def main():
    teste_y = 50
    teste_x = 50
    engine = Engine(screensize=(760,670), playerx=teste_x, playery=teste_y, gameversion="1.0", gamename="My Game")
    engine.screencolor = (255,255,255)

    engine.functions["Player"] = """self.player = ObjSquare(self.player_x,self.player_y,50,50,(0,0,0),5).draw(self.screen)"""
    engine.objects["Wall"] = ObjSquare(0,400,760,50,(255,0,0),50)
    engine.functions["Collision"] = """
player_antx = self.player_x
player_anty = self.player_y
self.PlayerMoveWASD()
player_rect = pg.Rect(self.player_x, self.player_y, 50, 50)
wall_rect = pg.Rect(0, 400, 760, 50)
if self.check_collision(player_rect, wall_rect):
    self.player_y = player_anty
    self.player_x = player_antx"""
    engine.run()

main()
