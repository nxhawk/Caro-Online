SIZE_TABLE = 20


def won(table):
    # check row
    for i in range(SIZE_TABLE):
        for j in range(SIZE_TABLE - 4):
            count_x = count_y = 0
            for k in range(j, j+5):
                if table[i][k] == 'X':
                    count_x += 1
                elif table[i][k] == 'O':
                    count_y += 1
                else:
                    break
            if count_x == 5:
                return 1
            if count_y == 5:
                return 2
    # check col
    for i in range(SIZE_TABLE):
        for j in range(SIZE_TABLE - 4):
            count_x = count_y = 0
            for k in range(j, j+5):
                if table[k][i] == 'X':
                    count_x += 1
                elif table[k][i] == 'O':
                    count_y += 1
                else:
                    break
            if count_x == 5:
                return 1
            if count_y == 5:
                return 2
    # check /
    for i in range(SIZE_TABLE - 4):
        for j in range(SIZE_TABLE - 4):
            count_x = count_y = 0
            for k in range(5):
                if table[i+k][j+k] == 'X':
                    count_x += 1
                elif table[i+k][j+k] == 'O':
                    count_y += 1
                else:
                    break
            if count_x == 5:
                return 1
            if count_y == 5:
                return 2
    # check \
    for i in range(SIZE_TABLE - 4):
        for j in range(SIZE_TABLE - 1, 5, -1):
            count_x = count_y = 0
            for k in range(5):
                if table[i+k][j-k] == 'X':
                    count_x += 1
                elif table[i+k][j-k] == 'O':
                    count_y += 1
                else:
                    break
            if count_x == 5:
                return 1
            if count_y == 5:
                return 2
    return -1
