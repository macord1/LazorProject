from itertools import permutations
from itertools import combinations
import copy
import numpy as np
'''
SOFTWARE CARPENTRY LAZOR PROJECT

Molly Accord
Sreelakshmi Sunil

'''

'''
Computes solutions from bff file of lazor game.
Solutions are saves as a text file - solution.txt
Separate unit_tests.py file is used for performing tests.
'''


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


class Block:

    '''
    Performs block operations such as reading bff files and saving the solution
    '''

    def __init__(self, File):
        '''
        Stores the name of bff file to file_name

        ***Parameters***
            File: the passed bff files from the main loop

        ***Returns***
            none
        '''
        self.file_name = File

    def Read_file(self):
        '''
        Reads the bff file, converts the grid to a matrix and stores concerned values to variables

        ***Parameters***
            File: the passed bff files from the main loop

        ***Returns***
            grid_matrix : converted board to matrix
            A (list): count of movable reflect blocks
            B (list): count of movable opaque blocks
            C (list): count of movable refract blocks
            L (tupule): coordinates of laser starting points and vx,vy explaining direction of laser
            P (tupule) : coordinates of points that laser must intersect
        '''

        GRID = []
        A = 0
        B = 0
        C = 0
        L = []
        P = []

        # openining the game bff file to read and store
        bff = open(self.file_name, "r")
        # reading all lines
        lines = bff.readlines()
        total_lines = len(lines)

        # converting grid to a matrix
        for i in range(total_lines):
            separated = lines[i].strip('\n')

            # starts at 'START' and ends at 'STOP'
            if separated == "GRID START":
                next_line = i + 1
                selected = lines[next_line].strip('\n')
                while selected != "GRID STOP":
                    row = selected.replace(" ", "")
                    GRID.append(row)
                    next_line = next_line + 1
                    selected = lines[next_line].strip('\n')

        # storing values of A, B, C as lists
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

        # intializing grid matrix as all zeros
        grid_matrix = np.zeros((height, width), dtype=int)

        for j in range(len(GRID)):

            for i in range(len(GRID[0])):

                if GRID[j][i] != "o":

                    value = GRID[j][i]

                    new_j = j * 2 + 1

                    new_i = i * 2 + 1

                    # Updating positions of centroids of fixed reflect, refract
                    # and opaque blocks as 31,51 and 41.
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


class Laser:

    '''
    Stores grid_matrix and performs various laser functions
    '''

    def __init__(self, Matrix):
        '''
        Stores the name of bff file to file_name

        ***Parameters***
            Matrix: the passed grid_matrix

        ***Returns***
            none
        '''
        self.grid_matrix = Matrix
        self.size1 = len(self.grid_matrix[0])
        self.size2 = len(self.grid_matrix)

    def valid_pos(self, x, y):
        '''
        Returns True if the coordinates specified (x and y) are within the matrix.
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
        return x >= 0 and x < self.size1 and y >= 0 and y < self.size2

    def incident__side(self, y, x, val):
        '''
        Computes and returns the side of block where the laser hits

        *** Parameters ***
            y (int): y coordinate of current laser position
            x (int): x coordinate of current laser position
            val (int): assigned value for centroid according to the block

        *** Returns ***

        incident_side(string) : Right, Left , Up or Down
        '''

        if self.grid_matrix[y][x + 1] == val:
            return 'left'
        elif self.grid_matrix[y][x - 1] == val:
            return 'right'
        elif self.grid_matrix[y - 1][x] == val:
            return 'down'
        elif self.grid_matrix[y + 1][x] == val:
            return 'up'
        else:
            pass

    def reflect(self, side, vx, vy):
        '''
        Alters vx, vy from L for reflection

        *** Parameters***
            side(string) : side of block where the laser hits
            vx (int) : direction x coordinate of laser
            vy (int) : direction y coordinate of laser

        *** Returns ***
            vx (int) : updated direction x coordinate of laser
            vy (int) : updated direction y coordinate of laser
        '''

        if side == 'left' or side == 'right':
            # only vy inverts , vx remains same in (vy,vx)
            vx = vx * -1

        elif side == 'up' or side == 'down':
            # only vy inverts , vx remains same in (vy,vx)
            vy = vy * -1

        else:
            pass

        return(vx, vy)

    def intial_values(self, vx, vy, temp_x, temp_y):
        '''
        Calculates the next cell using vx,vy

        *** Parameters ***
            vx (int) : direction x coordinate of laser
            vy (int) : direction y coordinate of laser
            temp_y (int): y coordinate of current laser position
            temp_x (int): x coordinate of current laser position

        *** Returns ***
            temp_y (int): updated y coordinate of (next) laser position
            temp_x (int): updated x coordinate of (next) laser position

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

    def check_allhit(self, P):
        '''
        Checks if all points that the laser must intersect are intersected

        *** Parameters ***
            P (tupule) : coordinates of points that laser must intersect

        *** Returns ***
            True : if all points that the laser must intersect are intersected
            False : if all points that the laser must intersect are not intersected

        '''

        for i in range(0, len(P)):

            temp_P = P[i]
            xx = temp_P[0]
            yy = temp_P[1]

            if self.grid_matrix[yy][xx] != 11:
                return False

            else:
                continue

        return True


def block_change(matrix_copy, A, B, C):
    '''
    Computes all possible positions for movable blocks using
    permutation and combination

    *** Parameters ***
        matrix_copy : grid_matrix intially read from the bff file
        A (list): count of movable reflect blocks
        B (list): count of movable opaque blocks
        C (list): count of movable refract blocks
    ***Returns***
        movBlocks_count (int) : total number of movable blocks
        centroid_comb (list of lists) : all possible movBlocks_count centroid combinations
        blocks_perm (list of lists) : all posible orders of movable blocks

    '''
    centroids_avail = []

    # storing coordinates of all possible centroids
    for i in range(1, len(matrix_copy) - 1, 2):
        for j in range(1, len(matrix_copy[0]) - 1, 2):

            # checks if any of the centroids are blocks
            if matrix_copy[i][j] == 0:
                centroids_avail.append([i, j])

            else:
                continue

    # total no. of movable blocks
    movBlocks_count = A + B + C

    # possible combinations for available centroids
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

    # all possible arragements for movable blocks
    blocks_comb = permutations(blocks_list, movBlocks_count)

    a = []

    for i in list(blocks_comb):
        a.append(i)

    blocks_perm = []

    # to avoid repeated tupules in permutations
    for i in a:
        if i not in blocks_perm:
            blocks_perm.append(i)

    return(centroid_comb, blocks_perm, movBlocks_count)


def make_cross(grid_matrix):
    '''
    To make a cross shape for the blocks

    *** Parameters ***
        grid_matrix : converted board to matrix

    *** Returns ***
        None
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


def laser_path(temp_y, temp_x, vx, vy, grid_matrix):
    '''
    Determines the path of a laser
    Depends on starting points of laser, reflective,
    refractive and opaque blocks.

    *** Parameters***
        vx (int) : direction x coordinate of laser
        vy (int) : direction y coordinate of laser
        temp_y (int): y coordinate of current laser position
        temp_x (int): x coordinate of current laser position
        grid_matrix : converted board to matrix

    *** Returns ***
        None

    '''
    # vx1, vy1, temp_x1, temp_y1 used only in case of refract blocks
    vx1 = 0
    vy1 = 0

    Lazor = Laser(grid_matrix)

    while True:
        temp_x, temp_y = Lazor.intial_values(vx, vy, temp_x, temp_y)
        if Lazor.valid_pos(temp_x, temp_y):
            # check only if the coordinates are possible
            if grid_matrix[temp_y][temp_x] in {0, 1, 10, 20}:
                # to set the lazer path until there is a block
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 30 or grid_matrix[temp_y][temp_x] == 31:
                # when there is a reflect block
                Lazor = Laser(grid_matrix)
                try:
                    side = Lazor.incident__side(
                        temp_y, temp_x, grid_matrix[temp_y][temp_x])
                    vx, vy = Lazor.reflect(side, vx, vy)

                except IndexError:
                    continue
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 50 or grid_matrix[temp_y][temp_x] == 51:
                # when there is a refract block
                Lazor = Laser(grid_matrix)
                try:
                    side = Lazor.incident__side(
                        temp_y, temp_x, grid_matrix[temp_y][temp_x])
                    # code to refract laser
                    temp_y1 = temp_y
                    temp_x1 = temp_x
                    vx1 = vx
                    vy1 = vy

                    while True:
                        temp_x1, temp_y1 = Lazor.intial_values(
                            vx1, vy1, temp_x1, temp_y1)
                        if Lazor.valid_pos(temp_x1, temp_y1):
                            # checks only if the coordinates are possible
                            if grid_matrix[temp_y1][temp_x1] in {0, 1, 10, 20}:
                                # to set the lazer path until there is a block
                                grid_matrix[temp_y1][temp_x1] = 11
                            else:
                                continue
                        # breaks out of loop if temp_x1, temp_y1 is out of matrix size range
                        else:
                            break

                    # calling reflect function
                    vx, vy = Lazor.reflect(side, vx, vy)
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


def save_solution(grid_matrix):
    '''
    Coverts and saves the obtained solution as a text file

    *** Parameters ***
        grid_matrix (matrix): final solved matrix
        solution (txt file) : text file with the solution for the bff file

    *** Returns ***
        None
    '''

    # to save solution into a text file
    text_file = open("solution.txt", "w")
    # deleting any previous content in the file
    text_file.truncate(0)

    # STORING THE POSITIONS OF MOVABLE BLOCKS IN ORGINAL BOARD

    opaque_blocks = []
    reflect_blocks = []
    refract_blocks = []

    for i in range(1, len(grid_matrix) - 1, 2):
        for j in range(1, len(grid_matrix[0]) - 1, 2):

            # checks if any of the centroids are movable blocks
            if grid_matrix[i][j] == 30:
                reflect_blocks.append([i, j])

            elif grid_matrix[i][j] == 40:
                opaque_blocks.append([i, j])

            elif grid_matrix[i][j] == 50:
                refract_blocks.append([i, j])

            else:

                continue

    text_file.write("THE POSITIONS OF MOVABLE BLOCKS IN ORGINAL BOARD \n\n")

    if len(reflect_blocks) != 0:

        text_file.write("\nPosition of Movable Reflect Blocks on board: \n")

        for i in reflect_blocks:
            # storing positions of blocks in actual board
            row = i[0] // 2 + 1
            col = i[1] // 2 + 1

            text_file.write("Position %d from left in row %d \n" % (col, row))

    if len(refract_blocks) != 0:

        text_file.write("\nPosition of Movable Refract Blocks on board: \n")

        for i in refract_blocks:
            # storing positions of blocks in actual board
            row = i[0] // 2 + 1
            col = i[1] // 2 + 1

            text_file.write("Position %d from left in row %d \n" % (col, row))

    if len(opaque_blocks) != 0:

        text_file.write("\nPosition of Movable Opaque Blocks on board: \n")

        for i in opaque_blocks:
            # storing positions of blocks in actual board
            row = i[0] // 2 + 1
            col = i[1] // 2 + 1

            text_file.write("Position %d from left in row %d \n" % (col, row))

    # create empty arrays for all info needed in text file
    open_blocks = []
    unfixed_A_blocks = []
    unfixed_B_blocks = []
    unfixed_C_blocks = []
    fixed_A_blocks = []
    fixed_B_blocks = []
    fixed_C_blocks = []
    Laser_start = []
    Laser_reach = []
    path = []

    # store value types in their respective array
    for i in range(0, len(grid_matrix)):
        for j in range(0, len(grid_matrix[0])):

            if (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 0:
                open_blocks.append((j, i))

            elif (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 30:
                unfixed_A_blocks.append((j, i))

            elif (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 40:
                unfixed_B_blocks.append((j, i))

            elif (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 50:
                unfixed_C_blocks.append((j, i))

            elif (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 31:
                fixed_A_blocks.append((j, i))

            elif (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 41:
                fixed_B_blocks.append((j, i))

            elif (i % 2) != 0 and (j % 2) != 0 and grid_matrix[i][j] == 51:
                fixed_C_blocks.append((j, i))

            elif grid_matrix[i][j] == 10:
                Laser_start.append((j, i))

            elif grid_matrix[i][j] == 11:
                path.append((j, i))

            for k in range(0, len(P)):
                temp_P = P[k]
                if i == temp_P[1] and j == temp_P[0]:
                    Laser_reach.append((j, i))

    # write text file

    text_file.write("\n\n\nOTHER MISCELLANEOUS INFORMATION \n\n")
    text_file.write("Open blocks at x,y positions: ")
    text_file.write(str(open_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("unfixed A blocks, or reflect blocks at x,y positions: ")
    text_file.write(str(unfixed_A_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("unfixed B blocks, or opaque blocks at x,y positions: ")
    text_file.write(str(unfixed_B_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("unfixed C blocks, or refract blocks at x,y positions: ")
    text_file.write(str(unfixed_C_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("fixed A blocks at x,y positions: ")
    text_file.write(str(fixed_A_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("fixed B blocks at x,y positions: ")
    text_file.write(str(fixed_B_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("fixed C blocks at x,y positions: ")
    text_file.write(str(fixed_C_blocks))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("Laser(s) start at x,y positions: ")
    text_file.write(str(Laser_start))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("Laser(s) passes through x,y positions: ")
    text_file.write(str(path))
    text_file.write("\n")
    text_file.write("\n")

    text_file.write("Laser(s) pass through desired at x,y positions: ")
    text_file.write(str(Laser_reach))
    text_file.write("\n")
    text_file.write("\n")

    text_file.close()


if __name__ == "__main__":

    '''
    Main Function

    Repeatedly checks if the game can be solved by inputing all
    possible combinations of movable blocks

    '''
    # to read bff file
    block = Block("mad_1.bff")
    grid_matrix, A, B, C, L, P = block.Read_file()

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

    # stores all possible combinations of movable blocks
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
            # coverting centroids to cross for laser_path
            make_cross(grid_matrix)

            # updating laser positions
            for m in range(0, len(L)):

                temp_L = L[m]
                L_x = temp_L[0]
                L_y = temp_L[1]
                vxx = temp_L[2]
                vyy = temp_L[3]

                # testing laser path for new combination of blocks
                laser_path(L_y, L_x, vxx, vyy, grid_matrix)

            # calling Laser class
            Lazor = Laser(grid_matrix)
            # checking if all points are hit by laser
            if Lazor.check_allhit(P):
                f = 1
                break
            else:
                continue
        # checking if the game is solved
        if f == 1:
            print("Solved")
            print("Look for the 'solutions' text file")
            break

        else:
            continue

    if f == 0:
        print("\nError : Not solved")

    save_solution(grid_matrix)
