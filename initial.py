import numpy as np
import random


def Read_file(file_name):

    GRID = []
    A = 0
    B = 0
    C = 0
    L = []
    P = []

    bff = open(file_name, "r")
    lines = bff.readlines()
    total_lines = len(lines)

    for i in range(total_lines):
        separated = lines[i].strip('\n')

        if separated == "GRID START":
            next_line = i + 1
            selected = lines[next_line].strip('\n')
            while selected != "GRID STOP":
                row = selected.replace(" ", "")
                GRID.append(row)
                next_line = next_line + 1
                selected = lines[next_line].strip('\n')

    for i in range(next_line + 1, total_lines):
        separated = lines[i].strip('\n')
        try:
            if separated[0] == "A":
                A = int(separated[2])
            elif separated[0] == "B":
                B = int(separated[2])
            elif separated[0] == "C":
                C = int(separated[2])
            elif separated[0] == "L":
                if separated[6] == "-" and separated[9] == "-":
                    L_row = (int(separated[2]), int(separated[4]),
                             -1 * int(separated[7]), -1 * int(separated[10]))
                elif separated[6] == "-" and separated[9] != "-":
                    L_row = (int(separated[2]), int(separated[4]),
                             -1 * int(separated[7]), int(separated[9]))
                elif separated[6] != "-" and separated[8] == "-":
                    L_row = (int(separated[2]), int(separated[4]),
                             int(separated[6]), -1 * int(separated[9]))
                else:
                    L_row = (int(separated[2]), int(separated[4]),
                             int(separated[6]), int(separated[8]))
                L.append(L_row)
            elif separated[0] == "P":
                P_row = (int(separated[2]), int(separated[4]))
                P.append(P_row)
        except IndexError:
            continue

    width = 2 * len(GRID[0]) + 1
    height = 2 * len(GRID) + 1

    grid_matrix = np.zeros((height, width), dtype=int)
    for j in range(len(GRID)):
        for i in range(len(GRID[0])):
            if GRID[j][i] != "o":
                value = GRID[j][i]
                new_j = j * 2 + 1
                new_i = i * 2 + 1
                if value == "A":
                    grid_matrix[new_j][new_i] = 31  # 30 represents A block
                elif value == "B":
                    grid_matrix[new_j][new_i] = 41  # 40 represents B block
                elif value == "C":
                    grid_matrix[new_j][new_i] = 51  # 50 represents C block
                elif value == "x":
                    grid_matrix[new_j][new_i] = 1  # 1 represents x block
            else:
                continue

    if A > 0:
        i = 1
        for m in range(1, len(grid_matrix) - 1, 2):
            for n in range(1, len(grid_matrix[0]) - 1, 2):
                if i > A:
                    break
                elif grid_matrix[m][n] == 0:
                    grid_matrix[m][n] = 30
                    i = i + 1
                else:
                    continue

    if B > 0:
        i = 1
        for m in range(1, len(grid_matrix) - 1, 2):
            for n in range(1, len(grid_matrix[0]) - 1, 2):
                if i > B:
                    break
                elif grid_matrix[m][n] == 0:
                    grid_matrix[m][n] = 40
                    i = i + 1
                else:
                    continue

    if C > 0:
        i = 1
        for m in range(1, len(grid_matrix) - 1, 2):
            for n in range(1, len(grid_matrix[0]) - 1, 2):
                if i > C:
                    break
                elif grid_matrix[m][n] == 0:
                    grid_matrix[m][n] = 50
                    i = i + 1
                else:
                    continue

    for i in L:
        grid_matrix[i[1]][i[0]] = 10

    for i in P:
        grid_matrix[i[1]][i[0]] = 20

    return(grid_matrix, A, B, C, L, P)


def block_moves(grid_matrix):

    moveable = []
    for m in range(1, len(grid_matrix) - 1, 2):
        for n in range(1, len(grid_matrix[0]) - 1, 2):
            if grid_matrix[m][n] == 30 or grid_matrix[m][n] == 40\
                    or grid_matrix[m][n] == 50 or grid_matrix[m][n] == 0:
                moveable.append(grid_matrix[m][n])
            else:
                continue

    random.shuffle(moveable)
    count = 0
    for m in range(1, len(grid_matrix) - 1, 2):
        for n in range(1, len(grid_matrix[0]) - 1, 2):
            if count == len(moveable):
                break
            elif grid_matrix[m][n] != 1 and grid_matrix[m][n] != 31\
                    and grid_matrix[m][n] != 41 and grid_matrix[m][n] != 51:
                grid_matrix[m][n] = moveable[count]
                count = count + 1
            else:
                continue

    print(grid_matrix)
    return grid_matrix


if __name__ == "__main__":
    output = Read_file("yarn_5.bff")
    block_moves(output[0])
