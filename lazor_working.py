import numpy as np
import random
import copy
from itertools import combinations
from itertools import permutations

# Assuming the following numbers for positions of a block
# possible paths, block allowed - 0
# no block allowed - 1
# laser starting points - 10
# laser path - 11
# Points we need tha laser to intersect - 20
# Reflect block - 30
# Opaque block - 40
# Refract block - 50
# Fixed reflect block - 31
# Fixed opaque block - 41
# Fixed refract block - 51


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

    return(grid_matrix, A, B, C, L, P)


def block_change(matrix_copy, A, B, C):

    centroids_avail = []

    for i in range(1, len(matrix_copy)-1, 2):
        for j in range(1, len(matrix_copy[0])-1, 2):

            # checks if any of the centroids are blocks
            if matrix_copy[i][j] == 0:
                centroids_avail.append([i, j])

            else:
                continue

    movBlocks_count = A + B + C

    centroid_comb = combinations(centroids_avail, movBlocks_count)

    blocks_list = []

    i = 0
    j = 0
    k = 0

    # inserting 30 as many times as A
    for i in range(0, A):
        blocks_list.append(30)
    # inserting 40 as many times as B
    for j in range(0, B):
        blocks_list.append(40)
    # inserting 50 as many times as C
    for k in range(0, C):
        blocks_list.append(50)

    blocks_comb = permutations(blocks_list, movBlocks_count)

    a = []

    # to avoid repeated permutations
    for i in list(blocks_comb):
        a.append(i)

    blocks_perm = []

    for i in a:
        if i not in blocks_perm:
            blocks_perm.append(i)

    return(centroid_comb, blocks_perm, movBlocks_count)


def valid_pos(x, y, size1, size2):
    '''
    possible_dirate if the coordinates specified (x and y) are within the matrix.
    taken from maze generation hw for software carpentry

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the matrix.
        y: *int*
            A y coordinate to check if it resides within the matrix.
        size: *int*
             length of the matrix (ie. len(matrix)).

    **Returns**

        possible_dir: *bool*
            Whether the coordiantes are possible_dir (True) or not (False).
    '''
    return x >= 0 and x < size1 and y >= 0 and y < size2


def make_cross(grid_matrix):
    '''
    To make a cross shape for the blocks 
    '''
    # To make cross
    for i in range(1, len(grid_matrix) - 1, 2):
        for j in range(1, len(grid_matrix[0]) - 1, 2):
            # checks if any of the centroids are blocks
            if grid_matrix[i][j] in {30, 31, 40, 41, 50, 51}:
                if grid_matrix[i][j - 1] in {0, 10, 20}:
                    grid_matrix[i][j - 1] = grid_matrix[i][j]
                if grid_matrix[i][j + 1] in {0, 10, 20}:
                    grid_matrix[i][j + 1] = grid_matrix[i][j]
                if grid_matrix[i - 1][j] in {0, 10, 20}:
                    grid_matrix[i - 1][j] = grid_matrix[i][j]
                if grid_matrix[i + 1][j] in {0, 10, 20}:
                    grid_matrix[i + 1][j] = grid_matrix[i][j]
            else:
                continue

    # To set common walls as refract
    for i in range(1, len(grid_matrix) - 1, 2):
        for j in range(1, len(grid_matrix[0]) - 1, 2):
            # checks if any of the centroids are blocks
            if grid_matrix[i][j] in {30, 31, 40, 41, 50, 51}:
                if grid_matrix[i][j - 1] != grid_matrix[i][j] and grid_matrix[i][j - 1] not in {10, 20}:
                    grid_matrix[i][j - 1] = 50
                if grid_matrix[i][j + 1] != grid_matrix[i][j] and grid_matrix[i][j + 1] not in {10, 20}:
                    grid_matrix[i][j + 1] = 50
                if grid_matrix[i - 1][j] != grid_matrix[i][j] and grid_matrix[i - 1][j] not in {10, 20}:
                    grid_matrix[i - 1][j] = 50
                if grid_matrix[i + 1][j] != grid_matrix[i][j] and grid_matrix[i + 1][j] not in {10, 20}:
                    grid_matrix[i + 1][j] = 50
            else:
                continue


def incident__side(y, x, val, grid_matrix):

    # Returns : right, left , up, down


    if grid_matrix[y][x+1] == val:
        return 'left'
    elif grid_matrix[y][x-1] == val:
        return 'right'
    elif grid_matrix[y-1][x] == val:
        return 'down'
    elif grid_matrix[y+1][x] == val:
        return 'up'
    else:
        pass


def reflect(side, temp_x, temp_y, vx, vy, grid_matrix):

    # to reflect right up

        # to reflect right up

    if side == 'left' or side == 'right':
        # only vy inverts , vx remains same in (vy,vx)
        vx = vx * -1

    elif side == 'up' or side == 'down':
        # only vy inverts , vx remains same in (vy,vx)
        vy = vy * -1

    else:
        pass

    return(vx, vy)


def intial_values(vx, vy, temp_x, temp_y):
    '''
    To calculate the next cell using vx,vy
    '''

    # (vx,vy)
    # (1, -1) - right up
    # (1, 1) - right down
    # (-1, 1) - left down
    # (-1, -1) - left up

    if (vx, vy) == (1, -1):
        temp_x = temp_x + 1
        temp_y = temp_y - 1

    elif (vx, vy) == (1, 1):
        temp_x = temp_x + 1
        temp_y = temp_y + 1

    elif (vx, vy) == (-1, 1):
        temp_x = temp_x - 1
        temp_y = temp_y + 1

    elif (vx, vy) == (-1, -1):
        temp_x = temp_x - 1
        temp_y = temp_y - 1

    else:
        print("invalid vx vy")

    return(temp_x, temp_y)


def laser_path(temp_y, temp_x, vx, vy, grid_matrix):

    # vx1, vy1, temp_x1, temp_y1 used only in case of refract blocks
    vx1 = 0
    vy1 = 0

    size1 = len(grid_matrix[0])
    size2 = len(grid_matrix)

    while True:
        temp_x, temp_y = intial_values(vx, vy, temp_x, temp_y)
        if valid_pos(temp_x, temp_y, size1, size2):
            # check only if the coordinates are possible
            if grid_matrix[temp_y][temp_x] in {0, 1, 10, 20}:
                # to set the lazer path until there is a block
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 30 or grid_matrix[temp_y][temp_x] == 31:
                # when there is a reflect block
                try:
                    side = incident__side(
                        temp_y, temp_x, grid_matrix[temp_y][temp_x], grid_matrix)
                    vx, vy = reflect(side, temp_x, temp_y, vx, vy, grid_matrix)

                except IndexError:
                    continue
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 50 or grid_matrix[temp_y][temp_x] == 51:
                # when there is a refract block
                try:
                    side = incident__side(
                        temp_y, temp_x, grid_matrix[temp_y][temp_x], grid_matrix)
                    # code to refract laser
                    temp_y1 = temp_y
                    temp_x1 = temp_x
                    vx1 = vx
                    vy1 = vy

                    while True:
                        temp_x1, temp_y1 = intial_values(
                            vx1, vy1, temp_x1, temp_y1)
                        if valid_pos(temp_x1, temp_y1, size1, size2):
                            # check only if the coordinates are possible
                            if grid_matrix[temp_y1][temp_x1] in {0, 1, 10, 20}:
                                # to set the lazer path until there is a block
                                grid_matrix[temp_y1][temp_x1] = 11
                            else:
                                continue
                        # breaks out of loop if temp_x1, temp_y1 is out of matrix size range
                        else:
                            break

                    # calling reflect function
                    vx, vy = reflect(side, temp_x, temp_y, vx, vy, grid_matrix)
                except IndexError:
                    continue
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 40 or grid_matrix[temp_y][temp_x] == 41:
                # when there is an opaque block
                grid_matrix[temp_y][temp_x] = 11
                break

            else:
                continue

        # breaks out of loop if temp_x1, temp_y1 is out of matrix size range
        else:
            break


def check_allhit(grid_matrix, P):

    for i in range(0, len(P)):

        temp_P = P[i]
        xx = temp_P[0]
        yy = temp_P[1]

        if grid_matrix[yy][xx] != 11:
            return False

        else:
            continue

    return True



if __name__ == "__main__":

    grid_matrix, A, B, C, L, P = Read_file("dark_1.bff")

    # inserting 20 for the points that we need the laser to intersect
    for i in range(0, len(P)):

        temp_P = P[i]
        xx = temp_P[0]
        yy = temp_P[1]

        grid_matrix[yy][xx] = 20

    # Updating the positions of laser start and the points.

    # inserting 10 to laser start points in the matrix grid

    for i in range(0, len(L)):

        temp_L = L[i]
        L_x = temp_L[0]
        L_y = temp_L[1]
        vxx = temp_L[2]
        vyy = temp_L[3]

        grid_matrix[L_y][L_x] = 10

    matrix_copy = copy.deepcopy(grid_matrix)
    print("Please wait")

    centroid_comb, blocks_perm, movBlocks_count = block_change(
        matrix_copy, A, B, C)

    # setting flag = 0 to check for solution
    f = 0
    # taking centroid combinations

    for i in list(centroid_comb):

        # taking block combinations
        for j in range(0, len(blocks_perm)):
            grid_matrix = copy.deepcopy(matrix_copy)

            for k in range(0, movBlocks_count):
                # seting different block positions
                x_temp = i[k][0]
                y_temp = i[k][1]
                grid_matrix[x_temp][y_temp] = blocks_perm[j][k]

            # out of k loop
            make_cross(grid_matrix)
            # print(grid_matrix)

            for m in range(0, len(L)):

                temp_L = L[m]
                L_x = temp_L[0]
                L_y = temp_L[1]
                vxx = temp_L[2]
                vyy = temp_L[3]

                # testing laser path for new combination of blocks
                laser_path(L_y, L_x, vxx, vyy, grid_matrix)

            # checking if all points are hit by laser
            if check_allhit(grid_matrix, P):
                f = 1
                break
            else:
                continue

        if f == 1:
            print("solved")
            break

        else:
            continue

    if f == 0:
        print("\nNot solved")

    print("\n came out of functions")
    print(grid_matrix)
    
