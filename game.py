from menu import Login

import pygame
import sys
import socket

HOST = '127.0.0.1'
SERVER_PORT = 65432
FORMAT = 'utf8'

RED = (155, 0, 0)
BLUE = (223, 232, 3)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SIZE_TABLE = 20
WIDTH_TABLE = 30
X_START = 100
Y_START = 100

table = [[None]*SIZE_TABLE for _ in range(SIZE_TABLE)]

player = None
turned = None


def draw_table():
    for i in range(SIZE_TABLE):
        for j in range(SIZE_TABLE):
            if table[i][j] == 'X':
                pygame.draw.rect(
                    screen, RED, [X_START + i*WIDTH_TABLE, Y_START + j*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
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
    global w, client, turned
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
            screen, RED, [X_START + x*WIDTH_TABLE, Y_START + y*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
    elif table[x][y] == 'O':
        pygame.draw.rect(
            screen, BLUE, [X_START + x*WIDTH_TABLE, Y_START + y*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE])
    pygame.draw.rect(
        screen, BLACK, [X_START + x*WIDTH_TABLE, Y_START + y*WIDTH_TABLE, WIDTH_TABLE, WIDTH_TABLE], 1)

    msg = f"TICK {w} {x} {y}"
    client.sendall(msg.encode(FORMAT))
    turned = False


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


def run_game():
    global client, player, turned, w

    ok = True
    while ok:
        screen.fill(WHITE)
        draw_table()

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

        if (turned == False):
            msg = client.recv(1024).decode(FORMAT)
            msg = msg.split(' ')
            if (msg[0] == 'TICK'):
                turned = True
                table[int(msg[2])][int(msg[3])] = msg[1]

    client.close()


def connect_server():
    global client, turned, w
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
    else:
        turned = False
        w = 'O'
    run_game()


connect_server()
