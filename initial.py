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

    # parse through each row
    for j in range(len(GRID)):
        # parse through each column
        for i in range(len(GRID[0])):
            # check if there are any fixed blocks or no blocks allowed spots
            if GRID[j][i] != "o":
                value = GRID[j][i]
                # go to corresponding grid_matrix coordinate
                # refer to width and height calculations for understanding
                new_j = j * 2 + 1
                new_i = i * 2 + 1
                if value == "A":
                    grid_matrix[new_j][new_i] = 31  # 31 represents fixed A block
                elif value == "B":
                    grid_matrix[new_j][new_i] = 41  # 41 represents fixed B block
                elif value == "C":
                    grid_matrix[new_j][new_i] = 51  # 51 represents fixed C block
                elif value == "x":
                    grid_matrix[new_j][new_i] = 1  # 1 represents x block
            else:
                continue

    # if there are any reflect blocks, we need to add them in
    if A > 0:
        i = 1
        # parse through rows of grid-matrix that can contain a centroid
        for m in range(1, len(grid_matrix) - 1, 2):
            # parse through columns of grid-matrix that can contain a centroid
            for n in range(1, len(grid_matrix[0]) - 1, 2):
                # if we have already added all A blocks, stop loop
                if i > A:
                    break
                # only add to empty centroid spots
                elif grid_matrix[m][n] == 0:
                    grid_matrix[m][n] = 30
                    # count if we have added an A block
                    i = i + 1
                else:
                    continue

    # if there are any opaque blocks, we need to add them in
    if B > 0:
        i = 1
        # parse through rows of grid-matrix that can contain a centroid
        for m in range(1, len(grid_matrix) - 1, 2):
            # parse through columns of grid-matrix that can contain a centroid
            for n in range(1, len(grid_matrix[0]) - 1, 2):
                # if we have already added all B blocks, stop loop
                if i > B:
                    break
                # only add to empty centroid spots
                elif grid_matrix[m][n] == 0:
                    grid_matrix[m][n] = 40
                    # count if we have added an B block
                    i = i + 1
                else:
                    continue

    # if there are any refract blocks, we need to add them in
    if C > 0:
        i = 1
        # parse through rows of grid-matrix that can contain a centroid
        for m in range(1, len(grid_matrix) - 1, 2):
            # parse through columns of grid-matrix that can contain a centroid
            for n in range(1, len(grid_matrix[0]) - 1, 2):
                # if we have already added all C blocks, stop loop
                if i > C:
                    break
                # only add to empty centroid spots
                elif grid_matrix[m][n] == 0:
                    grid_matrix[m][n] = 50
                    # count if we have added an C block
                    i = i + 1
                else:
                    continue

    # add in all lazor point starts
    for i in L:
        grid_matrix[i[1]][i[0]] = 10

    # add in all lazor point ends
    for i in P:
        grid_matrix[i[1]][i[0]] = 20

    return(grid_matrix, A, B, C, L, P)


def block_moves(grid_matrix):

    # create an empty array for open 0 centroids and moveable blocks
    moveable = []
    # parse through rows of grid-matrix that can contain a centroid
    for m in range(1, len(grid_matrix) - 1, 2):
        # parse through columns of grid-matrix that can contain a centroid
        for n in range(1, len(grid_matrix[0]) - 1, 2):
            # if grid centroid value belongs to an open block or a moveable block
            if grid_matrix[m][n] == 30 or grid_matrix[m][n] == 40\
                    or grid_matrix[m][n] == 50 or grid_matrix[m][n] == 0:
                # add to moveable array
                moveable.append(grid_matrix[m][n])
            else:
                continue

    # random shuffle array
    random.shuffle(moveable)
    count = 0
    # parse through rows of grid-matrix that can contain a centroid
    for m in range(1, len(grid_matrix) - 1, 2):
        # parse through columns of grid-matrix that can contain a centroid
        for n in range(1, len(grid_matrix[0]) - 1, 2):
            # if we have already added all of the moveable numbers back in, stop loop
            if count == len(moveable):
                break
            # if grid value does not euqal to x block or fixed block
            elif grid_matrix[m][n] != 1 and grid_matrix[m][n] != 31\
                    and grid_matrix[m][n] != 41 and grid_matrix[m][n] != 51:
                # fill new centroid with a value from the shuffled moveable array
                grid_matrix[m][n] = moveable[count]
                # count the number of times this is done so as to not exceed the moveable array
                count = count + 1
            else:
                continue

    print(grid_matrix)
    return grid_matrix


if __name__ == "__main__":
    output = Read_file("yarn_5.bff")
    block_moves(output[0])
