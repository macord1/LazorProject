import numpy as np


# Assuming the following numbers for positions of a block
# possible paths, block allowed - 0
# no block allowed - 1
# laser starting points - 10
# laser path - 11
# Points we need tha laser to intersect - 20
# A, reflect block - 40
# B, opaque block - 40
# C, refract block - 50


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

        try:

            if separated[0] == "A":

                A = separated[2]

            elif separated[0] == "B":

                B = separated[2]

            elif separated[0] == "C":

                C = separated[2]

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

                    L_row = (separated[2], separated[4],

                             separated[6], separated[8])

                L.append(L_row)

            elif separated[0] == "P":

                P_row = (int(separated[2]), int(separated[4]))

                P.append(P_row)

        except IndexError:

            continue

    width = 2 * len(GRID[0]) + 1

    height = 2 * len(GRID) + 1

    grid_matrix = np.zeros((width, height), dtype=int)

    # print(grid_matrix)

    return(grid_matrix, A, B, C, L, P)


def pos_chk(x, y, size):
    '''
    possible_dirate if the coordinates specified (x and y) are within the matrix.

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
    return x >= 0 and x < size and y >= 0 and y < size


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
    	print("\n incorrect call in incident side func")


def reflect(side, temp_x, temp_y, vx, vy, grid_matrix):

    # to reflect right up

    if side == 'left' or side == 'right':
        # only vy inverts , vx remains same in (vy,vx)
        vx = vx * -1
        if grid_matrix[temp_y-1][temp_x-1] == 0:
            grid_matrix[temp_y-1][temp_x-1] = 11

    elif side == 'up' or side == 'down':
        # only vy inverts , vx remains same in (vy,vx)
        vy = vy * -1
        if grid_matrix[temp_y-1][temp_x-1] == 0:
            grid_matrix[temp_y-1][temp_x-1] = 11
    else:
        print("something wrong in reflect func ")

    return(temp_y-1, temp_x -1, vx, vy)

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

    elif (vx,vy) == (1, 1):
        temp_x = temp_x + 1
        temp_y = temp_y + 1

    elif (vx,vy) == (-1, 1):
        temp_x = temp_x - 1
        temp_y = temp_y + 1

    elif (vx,vy) == (-1, -1):
        temp_x = temp_x - 1
        temp_y = temp_y - 1

    else :
        print("invalid vx vy")

    return(temp_x, temp_y)



def laser_path(temp_y, temp_x, vx, vy, grid_matrix):

    # vx1, vy1, temp_x1, temp_y1 used only in case of refract blocks
    vx1 = 0; vy1 = 0;
    temp_x1 = 0; temp_y1 = 0;

    size = len(grid_matrix)

    while True:

        temp_x, temp_y = intial_values(vx, vy, temp_x, temp_y)

        if pos_chk(temp_x, temp_y, size):
            # check only if the coordinates are possible
            if grid_matrix[temp_y][temp_x] == 0:
                # to set the lazer path until there is a block
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 30:
                # when there is a reflect block
                side = incident__side(temp_y, temp_x, 30, grid_matrix)
                temp_y, temp_x, vx, vy = reflect(side, temp_x, temp_y, vx, vy, grid_matrix)

            elif grid_matrix[temp_y][temp_x] == 50:
                # when there is a refract block
                side = incident__side(temp_y, temp_x, 50, grid_matrix)

                #code to refract laser

                temp_y1 = temp_y; temp_x1 = temp_x;
                vx1 = vx; vy1 = vy;

                while True:

                    temp_x1, temp_y1 = intial_values(vx1, vy1, temp_x1, temp_y1)

                    if pos_chk(temp_x1, temp_y1, size):
                        # check only if the coordinates are possible
                        if grid_matrix[temp_y1][temp_x1] == 0:
                            # to set the lazer path until there is a block
                            grid_matrix[temp_y1][temp_x1] = 11
                        else:
                            continue

                    else:
                        break
                # calling reflect function
                temp_y, temp_x, vx, vy = reflect(side, temp_x, temp_y, vx, vy, grid_matrix)

            elif grid_matrix[temp_y][temp_x] == 40:
                # when there is an opaque block
                break
            else:
                continue

        else:
            break

if __name__ == "__main__":

    grid_matrix, count_reflect, count_opaque, count_refract, L, P = Read_file(
        "mad_1.bff")

    # Updating the positions of laser start and the points.

    # inserting 10 to laser start points in the matrix grid

    for i in range(0, len(L)):

        temp_L = L[i]
        x = temp_L[0]
        y = temp_L[1]
        vx = temp_L[2]
        vy = temp_L[3]

        grid_matrix[y][x] = 10

    # inserting 20 for the points that we need the laser to intersect
    for i in range(0, len(P)):

        temp_P = P[i]
        xx = temp_P[0]
        yy = temp_P[1]

        grid_matrix[yy][xx] = 20

    '''

    TESTING VALUES

    # grid_matrix[2][6] = 40
    # grid_matrix[2][7] = 40
    # grid_matrix[2][8] = 40
    # grid_matrix[3][6] = 40
    # grid_matrix[3][7] = 40
    # grid_matrix[3][8] = 40
    # grid_matrix[4][6] = 40
    # grid_matrix[4][7] = 40
    # grid_matrix[4][8] = 40

    grid_matrix[3][4] = 50
    grid_matrix[3][5] = 50
    grid_matrix[3][6] = 50
    grid_matrix[4][4] = 50
    grid_matrix[4][5] = 50
    grid_matrix[4][6] = 50
    grid_matrix[5][4] = 50
    grid_matrix[5][5] = 50
    grid_matrix[5][6] = 50

    # grid_matrix[3][4] = 40
    # grid_matrix[3][5] = 40
    # grid_matrix[3][6] = 40
    # grid_matrix[4][4] = 40
    # grid_matrix[4][5] = 40
    # grid_matrix[4][6] = 40
    # grid_matrix[5][4] = 40
    # grid_matrix[5][5] = 40
    # grid_matrix[5][6] = 40

    # grid_matrix[3][4] = 30
    # grid_matrix[3][5] = 30
    # grid_matrix[3][6] = 30
    # grid_matrix[4][4] = 30
    # grid_matrix[4][5] = 30
    # grid_matrix[4][6] = 30
    # grid_matrix[5][4] = 30
    # grid_matrix[5][5] = 30
    # grid_matrix[5][6] = 30
    '''


    print(grid_matrix)

    print("\n")

    laser_path(y, x, vx, vy, grid_matrix)

    print("came out of functions")

    print(grid_matrix)

    print("\n")
