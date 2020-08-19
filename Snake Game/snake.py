# improvements:
# add restrictions like: if going left, cant go right... etc (done)
# add snacks of different weights... 1,2 or 3
# add walls you cant pass through (done)
# add a border around the window, to show its solid
# draw snacks as circles


import math
import pygame
import random
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1  # dirnx and dirny for direction
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+self.dirnx,self.pos[1]+self.dirny)

    def draw(self,surface,eyes=False):
        dis = self.w//self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))  # making the cubes for body

        if eyes:  # Making the eyes
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i * dis + dis - radius*2, j * dis + 8)
            pygame.draw.circle(surface,(0,0,0),circleMiddle,radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class circle(object):
    def draw(self,surface):
        pygame.draw.circle(surface,(0,255,0),)

class snake(object):
    body = []  # set of cubes to create snake body, has cube objects
    turns = {}

    def __init__(self,color,pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed() #can address multiple key press

            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]

                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i,c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p) #remove the turn from the turn list when the last cube has made the turn
            else: #normal straight movement
                """ #Pass through walls
                if c.dirnx == -1 and c.pos[0]<=0: c.pos = (c.rows-1,c.pos[1]) #if it goes left off surface
                elif c.dirnx == 1 and c.pos[0]>= c.rows-1: c.pos = (0,c.pos[1]) #if it goes right off surface
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1) #if it goes up off surface
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0],0) #if it goes down off surface
                else: c.move(c.dirnx,c.dirny) #for general straight movement
                """
                # Comment this section below and uncomment the section above to pass through walls
                if c.dirnx == -1 and c.pos[0]<=0: lost() #if it goes left off surface
                elif c.dirnx == 1 and c.pos[0]>= c.rows-1: lost() #if it goes right off surface
                elif c.dirny == -1 and c.pos[1] <= 0: lost() #if it goes up off surface
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: lost() #if it goes down off surface
                else: c.move(c.dirnx,c.dirny) #for general straight movement

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx,tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self,surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface,True) # draws the eyes for the first cube, or the head
            else:
                c.draw(surface)


def drawGrid(w,rows,surface):
    sizeBtwn = w//rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface,(0,0,0),(x,0),(x,w))
        pygame.draw.line(surface, (0,0,0), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((255,255,255))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()


def randomSnack(rows,snake):
    positions = snake.body  # item is snake object

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        weight = random.randrange(3)
        if len(list(filter(lambda z:z.pos == (x,y),positions)))>0:
            continue
        else:
            break

    return(x,y)

def message_box(subject,content):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass

def lost():
    for x in range(len(s.body)):
        if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):  # the condition to lose
            print('Score: ', len(s.body))
            message_box('You Lost!', 'Score was '+ str(len(s.body))+'!\n'+'Play again')
            s.reset((10, 10))
            break

def main():
    global width,rows,s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width,width))  # This is our main surface
    s = snake((0,0,255),(10,10))
    flag = True
    snack = cube(randomSnack(rows,s),color=(0,255,0))
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(1)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = circle(randomSnack(rows,s),color=(0,255,0))
        lost()
        redrawWindow(win)

    pass

main()