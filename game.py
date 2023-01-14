from menu import Login

import pygame
import sys
import socket
import threading
from Won import won

HOST = '127.0.0.1'
SERVER_PORT = 65432
FORMAT = 'utf8'

GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)

SIZE_TABLE = 20
WIDTH_TABLE = 30
X_START = 100
Y_START = 100

table = [[None]*SIZE_TABLE for _ in range(SIZE_TABLE)]

player = None
turned = None
start_threading = None
ok = True


def Your_turn(w, color):
    if color == 0:
        value = yourTurn.render(w, True, RED)
    else:
        value = yourTurn.render(w, True, GREEN)
    screen.blit(value, [100, 40])
    value = name.render(player, True, BLACK)
    screen.blit(value, [500, 45])


def draw_table():
    for i in range(SIZE_TABLE):
        for j in range(SIZE_TABLE):
            if table[i][j] == 'X':
                pygame.draw.rect(
                    screen, PINK, [X_START + i*WIDTH_TABLE, Y_START + j*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
            elif table[i][j] == 'O':
                pygame.draw.rect(
                    screen, BLUE, [X_START + i*WIDTH_TABLE, Y_START + j*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
            pygame.draw.rect(
                screen, BLACK, [X_START + i*WIDTH_TABLE, Y_START + j*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE], 1)


def check_pos(pos):
    x, y = pos
    for i in range(SIZE_TABLE):
        vtx = X_START + i*WIDTH_TABLE
        if x >= vtx and x <= vtx + WIDTH_TABLE:
            for j in range(SIZE_TABLE):
                vty = Y_START + j*WIDTH_TABLE
                if y >= vty and y < vty + WIDTH_TABLE:
                    return (i, j)
    return (-1, -1)


def tick_v(pos):
    global w, client, turned, start_threading
    if turned == False:
        return
    x, y = check_pos(pos)
    if (x == -1 and y == -1):
        return
    if (table[x][y] == 'X' or table[x][y] == 'O'):
        return
    table[x][y] = w
    if table[x][y] == 'X':
        pygame.draw.rect(
            screen, PINK, [X_START + x*WIDTH_TABLE, Y_START + y*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
    elif table[x][y] == 'O':
        pygame.draw.rect(
            screen, BLUE, [X_START + x*WIDTH_TABLE, Y_START + y*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
    pygame.draw.rect(
        screen, BLACK, [X_START + x*WIDTH_TABLE, Y_START + y*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE], 1)

    msg = f"TICK {w} {x} {y}"
    client.sendall(msg.encode(FORMAT))
    turned = False
    start_threading = True


app = Login()
player = app.run()

if player is None:
    pygame.quit()
    sys.exit()
client = None
w = None

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Caro online")
clock = pygame.time.Clock()
yourTurn = pygame.font.SysFont("comicsansms", 35)
name = pygame.font.SysFont("comicsansms", 35)


def draw_tl(w):
    x = 65
    y = 55
    if w == 'X':
        pygame.draw.rect(
            screen, PINK, [x, y, WIDTH_TABLE, WIDTH_TABLE])

    else:
        pygame.draw.rect(
            screen, BLUE, [x, y, WIDTH_TABLE, WIDTH_TABLE])
    pygame.draw.rect(
        screen, BLACK, [x, y, WIDTH_TABLE, WIDTH_TABLE], 3)


def recv_mess():
    global turned, client, ok
    try:
        msg = client.recv(1024).decode(FORMAT)
    except:
        return
    msg = msg.split(' ')
    if (msg[0] == 'TICK'):
        turned = True
        table[int(msg[2])][int(msg[3])] = msg[1]
    if msg[0] == 'EXIT2':
        print('LOSE')
        ok = False
        client.sendall("EXIT".encode(FORMAT))


def run_game():
    global client, player, turned, w, start_threading

    win = None
    while ok:
        win = won(table=table)
        if win == 1:
            print("player 1 win")
            client.sendall('EXIT2'.encode(FORMAT))
            break

        if win == 2:
            client.sendall('EXIT2'.encode(FORMAT))
            print("Player 2 win")
            break
        screen.fill(WHITE)
        draw_table()
        draw_tl(w)
        if turned == False:
            Your_turn("Opponent's Turn", 0)
        else:
            Your_turn("Your Turn", 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.sendall('EXIT'.encode(FORMAT))
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and turned == True:
                pos = pygame.mouse.get_pos()
                tick_v(pos)
        pygame.display.update()
        clock.tick(30)

        if (turned == False and start_threading == True):
            start_threading = False
            thr = threading.Thread(target=recv_mess)
            thr.start()

    client.close()


def connect_server():
    global client, turned, w, start_threading
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('CLIENT SIDE')
    client.connect((HOST, SERVER_PORT))
    print('client address:', client.getsockname())
    msg = "USERNAME " + player
    client.sendall(msg.encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    if msg == 'PLAYER 1':
        turned = True
        w = 'X'
        start_threading = False
    else:
        turned = False
        w = 'O'
        start_threading = True
    run_game()


connect_server()
