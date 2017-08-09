"""
Author: Seth Deane
Date: 12/6/2016
Description: Stratego
"""
from classes import Piece
import pygame as pg
import random

"""
piece types
"""
water = '~'
empty = ' '
bomb = 'B'
flag = 'F'
spy = 'S'
marshal = '9'
general = '8'
colonel = '7'
major = '6'
captain = '5'
lieutenant = '4'
sergeant = '3'
miner = '2'
scout = '1'

"""
piece types allowed
"""
bomballowed = 6
flagallowed = 1
marshalallowed = 1
generalallowed = 1
colonelallowed = 2
majorallowed = 3
captainallowed = 4
lieutenantallowed = 4
sergeantallowed = 4
minerallowed = 5
scoutallowed = 8
spyallowed = 1

"""
misc. globals
"""
p1flag = False  # True = p1 win
p2flag = False  # True = p2 win
dim = 10
numpieces = 40  # 40
board = [[Piece() for x in range(dim)] for y in range(dim)]

"""
pygame colors
"""
aqua = (0, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
fuchsia = (255, 0, 255)
gray = (128, 128, 128)
green = (0, 128, 0)
lime = (0, 255, 0)
maroon = (128, 0, 0)
navy = (0, 0, 128)
olive = (128, 128, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
silver = (192, 192, 192)
teal = (0, 128, 128)
white = (255, 255, 255)
yellow = (255, 255, 0)

"""
pygame variables
"""
dispwidth = 800
dispheight = 520
surfacedim = (dispwidth, dispheight)
screen = pg.display.set_mode(surfacedim)
pg.display.set_caption('Stratego')
piecesize = 45
piecespacing = 50
piecethickness = 0

########################################################################################################################
########################################################################################################################
########################################################################################################################


def game_loop():
    """
    Playing around with graphics
    """
    running = True
    screen.fill(white)
    pg.event.set_blocked(pg.MOUSEMOTION)

    # flagI = pg.image.load('flag.png')
    # screen.blit(flagI, (300, 300))

    while running:
        for e in pg.event.get():
            # prints mouse position
            # if e.type == pg.MOUSEMOTION or e.type == pg.MOUSEBUTTONDOWN:
            #     print(str(e.pos[0]) + ' ' + ' ' + str(e.pos[1]))

            # if user closes the window, the program will exit
            if e.type == pg.QUIT:
                pg.quit()
                quit()

            showboard()
            pg.display.update()

            if e.type == pg.MOUSEBUTTONDOWN:
                pg.draw.rect(screen, white, (0, dispheight - 20, dispwidth, 40), 0)  # clears text
                origx, origy = getpos()
                # if the location selected is empty or water, then it will just wait for a new piece on the next loop
                if board[origy][origx].player == 1:
                    highlightpossiblemoves(origx, origy)
                    newx, newy = newpos(origx, origy)
                    playermovepiece(origx, origy, newx, newy)

        showboard()
        pg.display.update()


def gameintro():
    intro = True
    screen.fill(white)

    while intro:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                quit()
        largeText = pg.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = textobjects("STRATEGO", largeText)
        TextRect.center = ((dispwidth / 2), (dispheight / 2))
        button('Self-Setup', 200, 300, 100, 100, gray, red, selfsetup)
        button('Pre-Placed', 400, 300, 100, 100, gray, red, preplaced)
        screen.blit(TextSurf, TextRect)
        pg.display.update()


def playermovepiece(origx, origy, newx, newy):
    """
    checks for validity of general moves, then calls attack() to determine valid piece moves. Then calls AI to move
    their piece directly after.
    :param origx: original x position
    :param origy: original y position
    :param newx: new x position
    :param newy: new y position
    :return: none
    """
    if (board[origy][origx].rep != bomb) and \
            (board[origy][origx].rep != flag) and \
            (board[origy][origx].rep != water):
        if board[newy][newx].rep != water:
            if newx != origx or newy != origy:
                if board[newy][newx].player != 1:
                    attack(origx, origy, newx, newy)
                    showboard()
                    pg.display.update()
                    pg.time.wait(500)
                    AImovepiece()
                    printboard()
                else:
                    print("Don't attack your own men -- Try Again")
                    message("Don't attack your own men -- Try Again")
            else:
                print("That is an invalid move -- Try Again")
                message("That is an invalid move -- Try Again")

        else:
            print("Don't drown your men! -- Try Again")
            message("Don't drown your men! -- Try Again")
    else:
        print("You cannot move bombs or flags -- Try Again")
        message("You cannot move bombs or flags -- Try Again")


def AImovepiece():
    while True:
        origy = random.randint(0, 8)
        origx = random.randint(0, 9)
        newy = origy + 1    # will just move pieces up in a straight line currently
        newx = origx
        if board[newy][newx].rep != water:
            if (board[origy][origx].rep != bomb) and \
                    (board[origy][origx].rep != flag) and \
                    (board[origy][origx].rep != water):
                if newx != origx or newy != origy:
                    if board[newy][newx].player != 2:
                        if board[origy][origx].player == 2:
                            attack(origx, origy, newx, newy)
                            break


def attack(origx, origy, newx, newy):
    """
    Determines valid piece moves, then executes accordingly.
    :param origx: original x position
    :param origy: original y position
    :param newx: new x position
    :param newy: new y position
    :return: none
    """
    attacker = board[origy][origx].rep
    defender = board[newy][newx].rep
    piece = board[origy][origx]
    new = board[newy][newx]
    if piece.player != new.player:
        # reveal AI piece when player attacks
        if new.player == 2:
            showpiece(defender, newx * piecespacing, newy * piecespacing)
            pg.display.update()
            pg.time.wait(800)
        # reveal AI piece when AI attacks
        if new.player == 1:
            showpiece(attacker, origx * piecespacing, origy * piecespacing)
            pg.display.update()
            pg.time.wait(800)
        if defender == empty:
            board[origy][origx] = Piece(empty, 3)  # replace old piece location with an empty spot
            board[newy][newx] = Piece(piece.rep, piece.player)  # update the new location with the piece
        if (attacker != spy) and (defender != bomb and defender != flag and defender != spy and defender != empty and defender != water):
            if int(attacker) > int(defender):
                piece = board[origy][origx]
                board[origy][origx] = Piece(empty, 3)  # replace old piece location with an empty spot
                board[newy][newx] = Piece(piece.rep, piece.player)  # update the new location with the piece
            if int(attacker) < int(defender):
                board[origy][origx] = Piece(empty, 3)
            if int(attacker) == int(defender):
                board[origy][origx] = Piece(empty, 3)
                board[newy][newx] = Piece(empty, 3)
        if attacker == spy:
            if defender == marshal:
                board[origy][origx] = Piece(empty, 3)  # replace old piece location with an empty spot
                board[newy][newx] = Piece(piece.rep, piece.player)  # update the new location with the piece
            else:
                board[origy][origx] = Piece(empty, 3)
        if defender == bomb:
            if attacker == miner:
                board[origy][origx] = Piece(empty, 3)  # replace old piece location with an empty spot
                board[newy][newx] = Piece(piece.rep, piece.player)  # update the new location with the piece
            else:
                board[origy][origx] = Piece(empty, 3)
                board[newy][newx] = Piece(empty, 3)
        if defender == flag:
            board[origy][origx] = Piece(empty, 3)  # replace old piece location with an empty spot
            board[newy][newx] = Piece(piece.rep, piece.player)  # update the new location with the piece
            running = False
            if piece.player == 1:
                p1flag = True
                print("Player 1 won!")
            if piece.player == 2:
                p2flag = True
                print("Player 2 won!")
        if defender == spy:
            if attacker == marshal:
                board[origy][origx] = Piece(empty, 3)
            else:
                board[origy][origx] = Piece(empty, 3)  # replace old piece location with an empty spot
                board[newy][newx] = Piece(piece.rep, piece.player)  # update the new location with the piece
    pg.display.update()


def playerplacepiece(x, y, piece):
    """
    place pieces for player 1
    :return:
    """
    totalpiecesplaced = 0
    bombtotal = 0
    flagtotal = 0
    marshaltotal = 0
    generaltotal = 0
    coloneltotal = 0
    majortotal = 0
    captaintotal = 0
    lieutenanttotal = 0
    sergeanttotal = 0
    minertotal = 0
    scouttotal = 0
    spytotal = 0
    print("Player 1, SETUP YOUR BOARD FOR BATTLE!!!")
    while totalpiecesplaced < numpieces:
        if 0 <= y <= 3 and 0 <= x <= 9:
            if board[y][x].rep == empty:
                if piece == bomb or piece == flag or piece == marshal or piece == general or piece == colonel or \
                                piece == major or piece == captain or piece == lieutenant or piece == sergeant or \
                                piece == miner or piece == scout or piece == spy:
                    if piece == bomb and bombtotal < bomballowed:
                        bombtotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(bombtotal) + " out of " + str(bomballowed) + " bombs have been placed")
                    elif piece == flag and flagtotal < flagallowed:
                        flagtotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(flagtotal) + " out of " + str(flagallowed) + " flags have been placed")
                    elif piece == marshal and marshaltotal < marshalallowed:
                        marshaltotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(marshaltotal) + " out of " + str(marshalallowed) + " marshals have been placed")
                    elif piece == general and generaltotal < generalallowed:
                        generaltotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(generaltotal) + " out of " + str(generalallowed) + " generals have been placed")
                    elif piece == colonel and coloneltotal < colonelallowed:
                        coloneltotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(coloneltotal) + " out of " + str(colonelallowed) + " colonels have been placed")
                    elif piece == major and majortotal < colonelallowed:
                        majortotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(majortotal) + " out of " + str(majorallowed) + " majors have been placed")
                    elif piece == captain and captaintotal < captainallowed:
                        captaintotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(captaintotal) + " out of " + str(captainallowed) + " captains have been placed")
                    elif piece == lieutenant and lieutenanttotal < lieutenantallowed:
                        lieutenanttotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(lieutenanttotal) + " out of " + str(
                            lieutenantallowed) + " lieutenants have been placed")
                    elif piece == sergeant and sergeanttotal < sergeantallowed:
                        sergeanttotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(sergeanttotal) + " out of " + str(sergeantallowed) + " sergeants have been placed")
                    elif piece == miner and minertotal < minerallowed:
                        minertotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(minertotal) + " out of " + str(minerallowed) + " miners have been placed")
                    elif piece == scout and scouttotal < scoutallowed:
                        scouttotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(scouttotal) + " out of " + str(scoutallowed) + " scouts have been placed")
                    elif piece == spy and spytotal < spyallowed:
                        spytotal += 1
                        totalpiecesplaced += 1
                        board[y][x] = Piece(piece, 1).rep
                        printboard()
                        print(str(spytotal) + " out of " + str(spyallowed) + " spies have been placed")
                    else:
                        print("There are too many pieces of that type -- Try Again")
                else:
                    print("Invalid piece -- Try Again")
            else:
                print("There is already a piece there -- Try Again")
        else:
            print("Player 1 can only place pieces (0 <= x <= 9) and (0 <= y <= 3) -- Try Again")


def selfsetup():
    selfsetup = True
    screen.fill(white)

    while selfsetup:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                quit()
        placepiecebutton('F', 500, 50, piecesize, piecesize, gray, red)


        piece = board[recenty][recentx].rep
        playerplacepiece(recentx, recenty, piece)
        showboard()
        pg.display.update()


recentx = 0
recenty = 0


def placepiecebutton(rep, x, y, w, h, i, a):
    """
    place pieces for self setup
    :param rep: rep of piece
    :param x: x pos
    :param y: y pos
    :param w: width
    :param h: height
    :param i: initial color
    :param a: active color
    :return: newx, newy
    """
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(screen, a, (x, y, w, h))
        if click[0] == 1:
            pg.event.set_blocked(pg.MOUSEMOTION)
            pg.event.wait()
            message("Select a location for the piece")
            newx, newy = getpos()
            recentx = newx
            recenty = newy
            board[newy][newx] = Piece(rep, 1)
    pg.draw.rect(screen, i, (x, y, w, h))
    smallText = pg.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = textobjects(rep, smallText)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(TextSurf, TextRect)


"""
HELPER FUNCTIONS
"""

def preplaced():
    """
    prepopulates the board with a professional setup
    :return: none
    """
    autofillp1()
    autofillp2()
    game_loop()


def getpos():
    """
    get the original x and y position based on mouse click position
    :return: the original x and y position
    """
    x = 0
    y = 0

    for e in [pg.event.wait()] + pg.event.get():
        # get original x position of mouse and convert to coordinate in board[][]
        x = e.pos[0]
        x = (x * 2) // 100
        # get original y position of mouse and convert to coordinate in board[][]
        y = e.pos[1]
        y = (y * 2) // 100

    return x, y


def newpos(origx, origy):
    """
    get the new x and y position based on mouse click position and checks validity of move
    :param origx: original x position
    :param origy: original y position
    :return: the new x and y position
    """
    newx, newy = getpos()

    # only return the new values if they are in a valid location (1 tile in any direction)
    # will have to account for scouts being able to move many tiles eventually, as well as in highlight
    if (newx == origx + 1 and newy == origy) or (newx == origx - 1 and newy == origy) or \
            (newy == origy + 1 and newx == origx) or (newy == origy - 1 and newx == origx):
        return newx, newy
    else:
        newx = origx
        newy = origy
        return newx, newy


def showpiece(rep, xpiecelocation, ypiecelocation):
    smallText = pg.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = textobjects(rep, smallText)
    TextRect.center = ((xpiecelocation + (piecesize / 2)), (ypiecelocation + (piecesize / 2)))
    screen.blit(TextSurf, TextRect)


def showboard():
    for y in range(dim):
        ypiecelocation = y * (piecesize + 5)
        for x in range(dim):
            xpiecelocation = x * (piecesize + 5)
            # player 1
            if board[y][x].player == 1:
                pg.draw.rect(screen, red, (xpiecelocation, ypiecelocation, piecesize, piecesize), piecethickness)
                showpiece(board[y][x].rep, xpiecelocation, ypiecelocation)
            # player 2
            if board[y][x].player == 2:
                pg.draw.rect(screen, blue, (xpiecelocation, ypiecelocation, piecesize, piecesize), piecethickness)
            # empty
            if board[y][x].player == 3:
                pg.draw.rect(screen, gray, (xpiecelocation, ypiecelocation, piecesize, piecesize), piecethickness)
            # water
            if board[y][x].rep == water:
                pg.draw.rect(screen, navy, (xpiecelocation, ypiecelocation, piecesize, piecesize), piecethickness)


def highlightpossiblemoves(origx, origy):
    hspacing = 50
    posx = origx + 1
    negx = origx - 1
    posy = origy + 1
    negy = origy - 1
    p = board[origy][origx].player
    if p == 1:
        if posx < 10:
            if board[origy][posx].rep != water and board[origy][posx].player != p:
                pg.draw.rect(screen, yellow, (posx * hspacing + 1, origy * hspacing + 1, piecesize - 3, piecesize - 3), 4)
        if board[origy][negx].rep != water and board[origy][negx].player != p:
            pg.draw.rect(screen, yellow, (negx * hspacing + 1, origy * hspacing + 1, piecesize - 3, piecesize - 3), 4)
        if posy < 10:
            if board[posy][origx].rep != water and board[posy][origx].player != p:
                pg.draw.rect(screen, yellow, (origx * hspacing + 1, posy * hspacing + 1, piecesize - 3, piecesize - 3), 4)
        if board[negy][origx].rep != water and board[negy][origx].player != p:
            pg.draw.rect(screen, yellow, (origx * hspacing + 1, negy * hspacing + 1, piecesize - 3, piecesize - 3), 4)
    pg.display.update()
    pg.event.wait()


def printboard():
    """
    print the game board in ptui version
    :return: none
    """
    strq = ""
    for y in range(dim):
        for x in range(dim):
            strq += board[y][x].rep

    for i in range(0, len(strq), dim):
        if i < len(strq) - (dim - 1):
            print(' '.join(list(strq[i:i + dim])))
        else:
            print(' '.join(list(strq[i:])))

    print("-------------------")


def createemptyboard():
    """
    initializes the empty board and prints the board
    :return: none
    """
    for y in range(dim):
        for x in range(dim):
            board[x][y] = Piece(empty, 3)
    board[4][2] = Piece(water, 3)
    board[4][3] = Piece(water, 3)
    board[4][6] = Piece(water, 3)
    board[4][7] = Piece(water, 3)
    board[5][2] = Piece(water, 3)
    board[5][3] = Piece(water, 3)
    board[5][6] = Piece(water, 3)
    board[5][7] = Piece(water, 3)
    printboard()


def autofillp1():
    board[6][0] = Piece(marshal, 1)
    board[6][1] = Piece(captain, 1)
    board[6][2] = Piece(lieutenant, 1)
    board[6][3] = Piece(miner, 1)
    board[6][4] = Piece(scout, 1)
    board[6][5] = Piece(captain, 1)
    board[6][6] = Piece(scout, 1)
    board[6][7] = Piece(scout, 1)
    board[6][8] = Piece(scout, 1)
    board[6][9] = Piece(captain, 1)
    board[7][0] = Piece(sergeant, 1)
    board[7][1] = Piece(scout, 1)
    board[7][2] = Piece(colonel, 1)
    board[7][3] = Piece(colonel, 1)
    board[7][4] = Piece(general, 1)
    board[7][5] = Piece(scout, 1)
    board[7][6] = Piece(sergeant, 1)
    board[7][7] = Piece(bomb, 1)
    board[7][8] = Piece(bomb, 1)
    board[7][9] = Piece(lieutenant, 1)
    board[8][0] = Piece(major, 1)
    board[8][1] = Piece(scout, 1)
    board[8][2] = Piece(major, 1)
    board[8][3] = Piece(spy, 1)
    board[8][4] = Piece(captain, 1)
    board[8][5] = Piece(lieutenant, 1)
    board[8][6] = Piece(bomb, 1)
    board[8][7] = Piece(sergeant, 1)
    board[8][8] = Piece(lieutenant, 1)
    board[8][9] = Piece(scout, 1)
    board[9][0] = Piece(major, 1)
    board[9][1] = Piece(miner, 1)
    board[9][2] = Piece(miner, 1)
    board[9][3] = Piece(miner, 1)
    board[9][4] = Piece(sergeant, 1)
    board[9][5] = Piece(bomb, 1)
    board[9][6] = Piece(flag, 1)
    board[9][7] = Piece(bomb, 1)
    board[9][8] = Piece(bomb, 1)
    board[9][9] = Piece(miner, 1)


def autofillp2():
    board[0][0] = Piece(miner, 2)
    board[0][1] = Piece(miner, 2)
    board[0][2] = Piece(bomb, 2)
    board[0][3] = Piece(flag, 2)
    board[0][4] = Piece(bomb, 2)
    board[0][5] = Piece(miner, 2)
    board[0][6] = Piece(scout, 2)
    board[0][7] = Piece(bomb, 2)
    board[0][8] = Piece(miner, 2)
    board[0][9] = Piece(scout, 2)
    board[1][0] = Piece(sergeant, 2)
    board[1][1] = Piece(captain, 2)
    board[1][2] = Piece(lieutenant, 2)
    board[1][3] = Piece(bomb, 2)
    board[1][4] = Piece(lieutenant, 2)
    board[1][5] = Piece(colonel, 2)
    board[1][6] = Piece(major, 2)
    board[1][7] = Piece(sergeant, 2)
    board[1][8] = Piece(bomb, 2)
    board[1][9] = Piece(sergeant, 2)
    board[2][0] = Piece(scout, 2)
    board[2][1] = Piece(colonel, 2)
    board[2][2] = Piece(major, 2)
    board[2][3] = Piece(major, 2)
    board[2][4] = Piece(scout, 2)
    board[2][5] = Piece(general, 2)
    board[2][6] = Piece(spy, 2)
    board[2][7] = Piece(bomb, 2)
    board[2][8] = Piece(sergeant, 2)
    board[2][9] = Piece(lieutenant, 2)
    board[3][0] = Piece(captain, 2)
    board[3][1] = Piece(scout, 2)
    board[3][2] = Piece(marshal, 2)
    board[3][3] = Piece(miner, 2)
    board[3][4] = Piece(captain, 2)
    board[3][5] = Piece(scout, 2)
    board[3][6] = Piece(lieutenant, 2)
    board[3][7] = Piece(scout, 2)
    board[3][8] = Piece(scout, 2)
    board[3][9] = Piece(captain, 2)


def button(msg, x, y, w, h, i, a, action):
    """
    place button on the screen.
    :param msg: message on button
    :param x: x coord of button
    :param y: y coord of button
    :param w: width of button
    :param h: height of button
    :param i: non-hover color
    :param a: hover color
    :param action: function that button calls
    :return: none
    """
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pg.draw.rect(screen, a, (x, y, w, h))
        if click[0] == 1:
            action()
    else:
        pg.draw.rect(screen, i, (x, y, w, h))
    smallText = pg.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = textobjects(msg, smallText)
    TextRect.center = ((x + (w / 2)), (y  + (h / 2)))
    screen.blit(TextSurf, TextRect)


def message(text):
    font = pg.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = textobjects(text, font)
    textRect.top = dispheight - 20
    screen.blit(textSurf, textRect)
    pg.display.update()


def textobjects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


if __name__ == '__main__':
    pg.init()
    createemptyboard()
    gameintro()


    # # p1placepiece()
    # print("Now It's Time to PLAY")
    # while p1flag == 0 and p2flag == 0:
    #     p1movepiece()

