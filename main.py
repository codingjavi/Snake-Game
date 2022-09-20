#importing pygame
from curses import KEY_DOWN, KEY_LEFT
import math
from mimetypes import init
import random
from re import S
from this import s
import tkinter as tk
import pygame
from tkinter import messagebox



#class that emcompases the cubes actions
class cube(object):
    rows = 20
    w = 500
    #__init__ initializes the objects and its atributes
        #only takes in start parameter(10,10)
    def __init__(self, start, dirnx = 1, dirny = 0, color = ((255, 0, 0))):
        
        #self.pos is (10, 10)
        self.pos = start
        #the snake immeadiately starts moving to the right
        self.dirnx = 1
        self.dirny = 0
        #red
        self.color = color
    
    #changing dirnx and dirny
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        #changing position SETTING POSITION
            #self.pos[0] refers to the first number of the START variable in the __init__ function
            #adding self.dirnx (could be 1, 0, -1 = (right, nothing, left))
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    #pygame draws objects in their top left side SO we gotta figure out the distace we're going to draw the cubes
        #trying to draw the rectangle in an entire cube
    def draw1(self, surface, eyes=False):
        global color
        #tring to find distance between squares in grind
            #how many times does rows goes into w = 25
        dis = self.w // self.rows
        
        #i is 10
        i = self.pos[0]
        
        #j is 10
        j = self.pos[1]

        
        #drawing a rectangle(x ,y ,width, height)
            #(251, 251, 24, 24)
            #(251, 251) is the center
                #(i*dis+1, j*dis+1) is what makes (10,10) the center
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-1,dis-1))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



#snake is going to contain a list of cube objects ^ for the snake body
class snake(object):
    #list of cube objects
    body = []

    #dictionary(like a set method)
    turns = {}

    #what variables the class in taking in
    def __init__(self, color, pos):

        #define parameters
        self.color = color

        #the head is going to be a cube at pos
        #cube only takes in pos parameters
        #(10,10) goes into the cube class
            #(10,10) is middle and (0,0) is top left
        self.head = cube(pos)
        


        #appending the self.head cube object into the self.body list
        self.body.append(self.head)


        #directions where the snake is mooving(one of them always has to be 0)
        self.dirnx = 0
        self.dirny = 1

    #how the snake moves
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        print (self.head.pos[:])
        #looking for movement in keys
            #get_pressed is a list storing numbers for values of keys
            #only alows one key at a time to get pressed
        keys = pygame.key.get_pressed()

        #loops through all of the keys
        for key in keys:
            #if left key is pressed
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                
            #have to know where the head turned so the rest of the cubes in the body can turn at that point
                #storing (self.head.pos[:] (position of the head)(10,10)) to the turns dictionary
                #setting self.head.pos[:] (in self.turns list) = [self.dirnx, self.dirny](where we turned)
                    #self.head.pos[:] = (10,10)
                #so new turn at this position and it turned left(we know which direction it turned)

                #pos is a variable we took in from from __init__function 
                    #gave the pos variable to self.head so self.head.pos is the same

                    #self.head.pos[:] = (10,10)
                        #SO at (10,10) = [-1, 0]
                #turns is a dictionary
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            #elif because we only want one to act
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1

                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        #for each cube object in self.body
        for i,c in enumerate(self.body):

            #getting each objects position in self.body
                #pos is (10,10) for start
            p = c.pos[:]

            #if a (cube) position is in the turns dictionary(where we stored the self.head.pos[:] when we turned)
            if p in self.turns:

                #self.turn[self.head.pos[:]] = [self.dirnx, self,dirny]
                    #SO self.head.pos[:] = [self.dirnx, self.dirny]
                
                #turn(where we're mooving) = turns dictionary at index(p) which grabs dirnX & dirnY
                    #SO turn = (dirnx, dirny) 
                        #because self.turns[p] = self.turns[c.pos[:]] = self.turns[10,10]
                turn = self.turns[p]
                
                #call move method in cube class with (turn[0], turn[1]) parameters (which is dirnx, dirny)
                c.move(turn[0], turn[1])

                
                
                #if the loop gets to the last cube (last i) of the body(-1 bc of head)
                if i == len(self.body) -1:
                    
                    #deletes key p from turns dictionary so it doesn't keep turning when hitting that position
                    self.turns.pop(p)
            
            
            #check if they're off the edge of the screen
                #if position not in turn list (so not turning)
            else:
                #if cube object is going to the left and it's at the edge of the screen then put it to the right side of the screen
                    #pos[0] is the x-value
                if c.dirnx == -1 and c.pos[0] <= 0:
                    #putting it to the right of the sceen
                    c.pos =  (rows -1, c.pos[1])
                
                #if object going to the right
                elif c.dirnx == 1 and c.pos[0] >= rows-1:
                    c.pos = (0, c.pos[1])

                #going down
                    #rows is just 20
                elif c.dirny == 1 and c.pos[1] >= rows -1:
                    c.pos = (c.pos[0], 0)
                
                #going up
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows-1)
                


                #if it's not turning or hitting the edge of the screen
                else:
                    #then just keep going the same direction
                        #calling the move method in the cube class
                    c.move(c.dirnx, c.dirny)

    def draw(self, surface):
        
        #giving an index to every cube object in the self.body list
        for i, c in enumerate(self.body):
            #if the object in the list is the first one
            if i ==0:
                #calling the draw1 method in the cube class and giving it true for eyes
                c.draw1(surface, True)
            else:
                #calling the draw1 method in the cube class(actually draws the rectangle)
                c.draw1(surface)

    def addCube(self):
        #finding out where the last cube of the body is(-1 gives us last)
            #self.body becuase in the snake class
                #s.body if outside class
        tail = self.body[-1]
        #setting tails direction from dirnx and dirny from self.dirnx FROM MOVE method
            #getting dirnx and dirny form __init__
        dx = tail.dirnx
        dy = tail.dirny

    #checking which direction we're moving(dx, dy)
        #if adding it to the right,left, above, below of the tail(cube) 
            #AND    giving it the correct directions 
        #if dx(tails dirnx) == 1 and dy(tails dirny)
        if dx == 1 and dy == 0:
            #adding a new CUBE object which takes in start(which is x,y)
                #cube taking in the x of tail.pos -1(we put in pos)
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

 
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
    global rows, width, s, snack
    #fill black in black screen
    surface.fill((0,0,0))
    
    #calls the draw function in the snake class (which calls the draw1 method in the cube class)
    s.draw(surface)
    snack.draw1(surface)
    
    #drawing a grid with this functions
    drawGrid(width, rows, surface)

    
    #update game window bc there's been change
    pygame.display.update()

#item is the snake object
def randomSnack(rows, item):
    
    #positions is new list
    positions = item.body

    #LOOPING THRU EVERY POSITION IN THIS LIST and checking it against x and y
        #if its the SAME then LOOP AGAIN, if not then BREAK LOOP
    #chooses a random spot to put the snack in 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        #getting a list of a filtered list
            #and checking if any of the positions are equal to snakes current position
                #make sure it doesn't spawn a cube on top of the snake
                    #if this function zed positions == to the random position we generated
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            #gonna have to do it again
            continue
        else:
            break
    return (x,y)

#showing message when lost
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass




#runs game
def main():
    global rows, width, s, snack
    rows = 20
    width = 500
    #making a screen, width, width because its a square
    win = pygame.display.set_mode((width, width))

    #using the snake class to make it red and put it at (10, 10)
        #these parameters are going to the cube class(in the snake class)
    s = snake((250, 0, 0), (10, 10))


    #creating the snake object
        #giving it position from randomSnack function
            #takes in rows and intem(snake object)
                #making it green
    snack = cube(randomSnack(rows, s), color=((0,255,0)))
    
    #built in, helps slow down game
    clock = pygame.time.Clock()

    loop = True
    while loop:
        pygame.time.delay(50)
        
        #we only want the snake to move 10 blocks(frames) a second
        clock.tick(10)
        
        #calling this function to fill the screen black and call the drawGrid() fucntion
        redrawWindow(win)

        #calling the moving method in the snake class
        s.move()

        #checking to see if the head of snake hit a snack
        #s.body because from the snake class and .pos(parameter we gave to snake class) to get its position
            #snack.pos from self.pos = start from cube class
        if s.body[0].pos == snack.pos:
            #calling new snake class method
            s.addCube()
            #making a new snack
            snack = cube(randomSnack(rows, s), color=((0,255,0)))
        
        #going through body list 
        for x in range(len(s.body)):
            #if an object in the body list is in this list 
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #score is length of body
                print('Score:' , len(s.body))
                message_box('You Lost!, Play again..')
                s.reset((10,10))
                #break out of loop
                break

        #looking for events and quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

main()


    
    
