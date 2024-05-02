
from engine import *
import pygame as pg
from pygame.locals import *
from sys import exit

def main():
    game = Game((760,670),50,50,"1.0","testing events")
    game.screencolor = (255,255,255)
    game.gravity_force = 0.5
    
    game.events["OnGameStart"] = 'print("game started!")'
    game.filescripts.append("player")
    game.filescripts.append("playerphysics")

    game.Start()

main()
