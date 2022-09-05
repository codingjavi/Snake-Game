#importing pygame
import math
import random
import tkinter as tk
import pygame
from tkinter import messagebox

pygame.init()


class cube(object):
    rows = 0
    w = 0
    #__init__ initializes the objects and its atributes
    def __init__(self, start, dirnx = 1, dirny = 0, color = ((255, 0, 0))):
        pass

#snake is going to contain a list of cube objects ^ for the snake body
class snake(object):
    #list of cube objects
    body = []
    turns = ()

    #what variables the class in taking in
    def __init__(self, color, pos):
        #define parameters
        self.color = color

        #the head is going to be a cube at pos
        self.head = cube(pos)

        #we're going to append the body list onto the head
        #reference variables in class as self
        self.body.append(self.head)

        #directions where the snake is mooving
        self.dirnx = 0
        self.dirny = 1


def drawGrid(w, rows, surface):
    #gap between each line, using // to not get any decimal numbers bc draw line method won't take it
    size_between = w // rows

    x = 0
    y = 0 

    for i in range(rows):
        x = x + size_between
        y = y + size_between

        #using the pygame.draw.line method to create the rows and columns
        #they're going to be white, starts at (x, 0) and keep going down because the x is changing until (x,w)
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow(surface):
    global rows, width
    #fill black in black screen
    surface.fill((0,0,0))

    #drawing a grid with this functions
    drawGrid(width, rows, surface)

    #update game window bc there's been change
    pygame.display.update()

#runs game
def main():
    global rows, width
    rows = 20
    width = 500
    #making a screen, width, width because its a square
    win = pygame.display.set_mode((width, width))

    #using the snake class to make it red and put it at (10, 10)
    s = snake((250, 0, 0), (10, 10))

    #built in, helps slow down game
    clock = pygame.time.Clock()

    loop = True
    while loop:
        pygame.time.delay(50)
        
        #we only want the snake to move 10 blocks(frames) a second
        clock.tick(10)
        
        #calling this function to fill the screen black and call the drawGrid() fucntion
        redrawWindow(win)

        #looking for events and quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

main()

    
    
