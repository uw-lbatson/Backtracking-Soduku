import pygame
from random import randint
from sudokuGrids import *

#initialize pygame
pygame.init()

#x and y lengths for window size
screenX = 600
screenY = 600

#window size
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Sudoku")

#initialize solve variables for future use
x = 0
y = 0
value = 0
gridVal = 0

#set dif to be 9 equal parts that sum to screenX
dif = screenX / 9

#initialize font
font = pygame.font.SysFont("Arial", 30)

#number offsets for placing numbers in squares
xNumOffset = 26
yNumOffset = 15

#getCoordinate -> sets global x and y to the grids coordinate position
def getCoordinate(pos):
    global x
    x = pos[0]//dif
    global y
    y = pos[1]//dif

#drawSelectedCell -> encapsulates cell (x,y) in red square
def drawSelectedCell():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif, (y+i)*dif),
                         (x * dif + dif, (y+i)*dif), 2)
        pygame.draw.line(screen, (255, 0, 0), ((x+i)*dif, y*dif),
                         ((x+i)*dif, y * dif + dif), 2)

#makeLines -> draws the sudoku tiling on the board, filling in the grid with numbers
def makeLines(grid):
    for i in range(9):
        for j in range(9):
            #if cell (x,y) isnt empty
            if grid[i][j] != 0:
                #get cell number, and print to middle of cell
                boxNumber = font.render(str(grid[i][j]), 1, (0,0,0))
                screen.blit(boxNumber, (i*dif + xNumOffset, j*dif + yNumOffset))
                
    #prints thicker lines to indicate 3x3 squares         
    for i in range(10):
        #when on a multiple of 3, make line thickness greater
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, (0,0,0), (0, i*dif), (screenX, i*dif), thickness)
        pygame.draw.line(screen, (0,0,0), (i*dif, 0), (i*dif, screenX), thickness)

#validValue -> determines if value is valid in its row, column and 3x3 square
def validValue(grid, row, col, value):
    #gets coords of closest 3x3 square
    colSqr = col//3
    rowSqr = row//3

    #determine if any value in row and column contains value
    for i in range(9):
        if grid[row][i] == value:
            return False
        if grid[i][col] == value:
            return False

    #determine if corresponding 3x3 square contains value
    for i in range(rowSqr*3, rowSqr*3 + 3):
        for j in range(colSqr*3, colSqr*3 + 3):
            if grid[i][j] == value:
                return False
            
    #if value doesn't exist, value is correct  
    return True

#solveGrid -> solves grid using backtracking algorithm
def solveGrid(grid, row, col):
    #gets row and col value such that grid[row][col] is empty
    while grid[row][col] != 0:
        if (row<8):
            row += 1
        elif ((row == 8) and (col<8)):
            row = 0
            col += 1
        #if at final cell (8,8), grid must be solved
        elif ((row == 8) and (col == 8)):
            return True

    #prevents any events (keypresses / clicks) during the solution
    pygame.event.pump()

    #tests all possible values given row and col
    for k in range(1,10):
        #checks if valid value
        if (validValue(grid, row, col, k) == True):
            grid[row][col] = k
            global x, y
            x = row
            y = col
            
            #update screen to display new cell value
            screen.fill((255,255,255))
            makeLines(grid)
            drawSelectedCell()
            pygame.display.update()
            
            #add delay to show backtracking
            pygame.time.delay(10)
            
            #check if new number solves grid
            if (solveGrid(grid, row, col) == True):
                return True
            else:
                #if it doesnt solve grid, cant be right number
                grid[row][col] = 0

            #since not right number, update screen again to make cell empty
            screen.fill((255,255,255))
            makeLines(grid)
            drawSelectedCell()
            pygame.display.update()
            pygame.time.delay(10)

    #if not solved, function returns false      
    return False

#define running variable to run main loop
running = True

#define binary variables for easy variable manipulation
flag1 = 0
newGrid = 0
solve = 0
checkSolved = 0
empty = 0

#begin main loop
while running:
    #fill screen white
    screen.fill((255,255,255))

    #current sudoku grid is the index of gridVal from grids in sudokuGrids
    grid = grids[gridVal]

    #check for events (key press/mouse click)
    for event in pygame.event.get():
        #if event is quit, quit application
        if event.type == pygame.QUIT:
            run = False

        #if event is mouse click, flag1 = true for drawSelectedCell(), gets cell coord
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            position = pygame.mouse.get_pos()
            getCoordinate(position)
        #if event is key press...
        if event.type == pygame.KEYDOWN:
            #left key -> move selected coord left one
            if event.key == pygame.K_LEFT:
                x-=1
                flag1 = 1
            #right key -> move selected coord right one
            if event.key == pygame.K_RIGHT:
                x+=1
                flag1 = 1
            #up key -> move selected coord up one
            if event.key == pygame.K_UP:
                y-=1
                flag1 = 1
            #down key -> move selected coord down one
            if event.key == pygame.K_DOWN:
                y+=1
                flag1 = 1
                
            #keys 1-9 input possible value for cell
            if event.key == pygame.K_1:
                value = 1
            if event.key == pygame.K_2:
                value = 2
            if event.key == pygame.K_3:
                value = 3
            if event.key == pygame.K_4:
                value = 4
            if event.key == pygame.K_5:
                value = 5
            if event.key == pygame.K_6:
                value = 6
            if event.key == pygame.K_7:
                value = 7
            if event.key == pygame.K_8:
                value = 8
            if event.key == pygame.K_9:
                value = 9

            #g key -> gets new grid from grid list in sudokuGrids
            if event.key == pygame.K_g:
                newGrid = 1
            #s key -> solves current grid state with backtracking
            if event.key == pygame.K_s:
                solve = 1
            #k key -> determines if grid is solved or not
            if event.key == pygame.K_c:
                checkSolved = 1
            #e key -> empties cell
            if event.key == pygame.K_e:
                position = pygame.mouse.get_pos()
                getCoordinate(position)
                empty = 1
                

    #when keys 1-9 are pressed, if valid value, value is entered to cell
    if value != 0:
        if (validValue(grid, int(x), int(y), value) == True):
            grid[int(x)][int(y)] = value
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
        #reset value to 0 to prevent loop
        value = 0

    #when e is pressed, empty hovered cell
    if (empty == 1):
        grid[int(x)][int(y)] = 0
        empty = 0

    #if g key is pressed, get new grid by increasing gridVal in loop
    if (newGrid == 1):
        if (gridVal+1 > len(grids)-1):
            gridVal = 0
        else:
            gridVal += 1
        #reset value to 0 to prevent loop
        newGrid = 0

    #if s key is pressed, solve current grid with backtracking
    if (solve == 1):
        solveGrid(grid, 0, 0)
        if (solveGrid(grid, 0, 0) == False):
            print("Impossible grid!")
        solve = 0

    #if c key is pressed, checks if grid is solved
    if (checkSolved == 1):
        if (solveGrid(grid, 0, 0) == False):
            checkSolved = 0
            print("Not Solved!")
        else:
            checkSolved = 0
            print("Grid is solved!")

    #updates current grid
    makeLines(grid)

    #when cell is clicked, highlight cell with drawSelectedCell()
    if (flag1 == 1):
        drawSelectedCell()

    #updates pygame display
    pygame.display.update()

#exit pygame
pygame.quit()
