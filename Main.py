import pygame, sys, random, math, time
from pygame.locals import *
from pygame.compat import unichr_, unicode_
black = (0,0,0)
white = (250,250,250)
r = random.randint
cusSq = 0
pygame.init()
pygame.font.init()
# wordList = ['APPLES','PIES','VANILLA']
# wordList = ['APPLES']
# wordList = ['APPLES','APPLES']
# wordList = ['AAA','XXX','ZZZZZ']
# wordList = ['ZZZZZZZZZZZZZ','AAA','XXX']
wordList = []

def getInfo():
    print("What would you like to put into your word list?\nPress enter when you are done.")
    while True:
        error = False
        x = input("   : ").upper()
        if x == '':
            break
        for letter in x:
            if letter.isalpha() == False and error == False:
                error = True
                print("Please only use alphabetic characters.")
        if error == False:
            wordList.append(x)

cusSq = getInfo()

gridRes = 15
resolution = gridRes * 50
for x in wordList:
    if len(x) > gridRes:
        resolution = (len(x))*50
        gridRes = len(x)
# if cusSq > gridRes:
#     resolution = (cusSq)*50

winsurobj = pygame.display.set_mode((resolution+10,resolution+10))
pygame.display.set_caption("Wordsearch")
fpsClock = pygame.time.Clock()
background = pygame.Surface(winsurobj.get_size())
background = background.convert()
background.fill(white)
winsurobj.blit(background, (0, 0))
font = pygame.font.SysFont('None', 50)

grid = []
for i in range (0,gridRes*gridRes):
    grid.append('')

def LrudFix(coOrds,Lrud):
    x = coOrds[0]
    y = coOrds[1]
    if Lrud == 1:
        #left
        x += 1
    if Lrud == 2:
        #right
        x -= 1
    if Lrud == 3:
        #up
        y -= 1
    if Lrud == 4:
        #down
        y += 1
    return(x,y)

lst = 'lst'
xy = 'xy'
def ordFromNum(n,a):
    x = n
    if a == 'lst' and type(n) == tuple:
        x = n[0]
        x += n[1]*gridRes
    if a == 'xy' and type(n) == int:
        x = (n%gridRes,int(n/gridRes))
    return x

def rChr():
    return chr(random.randint(65,90))

def wordToList(grid,word,coOrds):
    for letter in word:
        coOrds = ordFromNum(coOrds,'lst')
        grid[coOrds] = letter
        coOrds = LrudFix(ordFromNum(coOrds,'xy'),1)
    return grid

def ordToScreen(xy):
    x = xy[0]
    y = xy[1]
    x = (x*50)+10
    y = (y*50)+10
    return (x,y)

def listToScreen(grid):
    xxx = 0
    for i in grid:
        text = font.render(i, 0, black)
        winsurobj.blit(text,ordToScreen(ordFromNum(xxx,'xy')))
        time.sleep(0.01)
        pygame.display.update()
        xxx+=1

def validSquare(newPoint,originPoint):
    nP = ordFromNum(newPoint,lst)
    x = True
    if grid[nP] != '':
        x = False
    if nP < 0:
        x = False
    if nP > len(grid):
        x = False
    if x == False:
        return False
    else:
        np = ordFromNum(nP,xy)
        op = ordFromNum(originPoint,xy)
        if int(np[0]) == int(op[0]):
            return True
        elif int(np[1]) == int(op[1]):
            return True
        else:
            return False

## This is where I randomly decide where to put things.
## I'll code that later.
for word in wordList:
    x=0
    while True:
        try:
            ## Pick a random point and a random direction
            point = pointF = ordFromNum((r(0,len(grid)-1)),xy)
            direction = r(1,4)
            for letter in word:
                pointF = LrudFix(pointF,direction)
                if validSquare(pointF,point) == False:
                    raise Exception('Fuck')
            for letter in word:
                grid[ordFromNum(point,lst)] = letter
                point = LrudFix(point,direction)
            break
        except:
            pass
        x+=1
        if x >= 50000:
            print("'"+word+"'"+" could not be added.")
            break

# xxx = 0
# for word in wordList:
#     grid = wordToList(grid,word,(0,xxx))
#     xxx+=1

xxx = 0
for i in grid:
    if i == '':
        grid = wordToList(grid,rChr(),xxx)
    xxx+=1

listToScreen(grid)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(30)
