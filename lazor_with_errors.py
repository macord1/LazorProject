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


    return(grid_matrix, A, B, C, L, P)


def valid_pos(x, y, size1, size2):
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
    return x >= 0 and x < size1 and y >= 0 and y < size2


def make_cross(grid_matrix):

    '''
    To make a cross shape for the blocks 
    '''
    # To make cross
    for i in range(1, len(grid_matrix), 2):
        for j in range(1, len(grid_matrix[0]), 2):
            
            #checks if any of the centroids are blocks
            if grid_matrix[i][j] in {30,31,40,41,50,51}:

                if grid_matrix[i][j-1] == 0:
                    grid_matrix[i][j-1] = grid_matrix[i][j]

                if grid_matrix[i][j+1] == 0:
                    grid_matrix[i][j+1] = grid_matrix[i][j]

                if grid_matrix[i-1][j] == 0:
                    grid_matrix[i-1][j] = grid_matrix[i][j]

                if grid_matrix[i+1][j] == 0:
                    grid_matrix[i+1][j] = grid_matrix[i][j]

            else:
                continue

    # To set common walls as opaque
    for i in range(1, len(grid_matrix), 2):
        for j in range(1, len(grid_matrix[0]), 2):
            
            #checks if any of the centroids are blocks
            if grid_matrix[i][j] in {30,31,40,41,50,51}:

                if grid_matrix[i][j-1] != grid_matrix[i][j] and grid_matrix[i][j-1] not in {10,20}:
                    grid_matrix[i][j-1] = 50
                if grid_matrix[i][j+1] != grid_matrix[i][j] and grid_matrix[i][j+1] not in {10,20}:
                    grid_matrix[i][j+1] = 50
                if grid_matrix[i-1][j] != grid_matrix[i][j] and grid_matrix[i-1][j] not in {10,20}:
                    grid_matrix[i-1][j] = 50
                if grid_matrix[i+1][j] != grid_matrix[i][j] and grid_matrix[i+1][j] not in {10,20}:
                    grid_matrix[i+1][j] = 50

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
        print("\n incorrect call in incident side func")


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
        print("something wrong in reflect func ")

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

    size1 = len(grid_matrix[0])
    size2 = len(grid_matrix)

    while True:

        temp_x, temp_y = intial_values(vx, vy, temp_x, temp_y)

        if valid_pos(temp_x, temp_y, size1, size2):
            # check only if the coordinates are possible
            if grid_matrix[temp_y][temp_x] in {0,1,10,20}:
                # to set the lazer path until there is a block
                grid_matrix[temp_y][temp_x] = 11

            elif grid_matrix[temp_y][temp_x] == 30 or grid_matrix[temp_y][temp_x] == 31 :
                # when there is a reflect block
                side = incident__side(temp_y, temp_x, grid_matrix[temp_y][temp_x], grid_matrix)
                vx, vy = reflect(side, temp_x, temp_y, vx, vy, grid_matrix)

            elif grid_matrix[temp_y][temp_x] == 50 or grid_matrix[temp_y][temp_x] == 51:
                # when there is a refract block
                side = incident__side(temp_y, temp_x, grid_matrix[temp_y][temp_x], grid_matrix)

                #code to refract laser

                temp_y1 = temp_y; temp_x1 = temp_x;
                vx1 = vx; vy1 = vy;

                while True:

                    temp_x1, temp_y1 = intial_values(vx1, vy1, temp_x1, temp_y1)

                    if valid_pos(temp_x1, temp_y1, size1, size2):
                        # check only if the coordinates are possible
                        if grid_matrix[temp_y1][temp_x1] == 0:
                            # to set the lazer path until there is a block
                            grid_matrix[temp_y1][temp_x1] = 11
                        else:
                            continue
                    # breaks out of loop if temp_x1, temp_y1 is out of matrix size range
                    else:
                        break
                # calling reflect function
                vx, vy = reflect(side, temp_x, temp_y, vx, vy, grid_matrix)

            elif grid_matrix[temp_y][temp_x] == 40 or grid_matrix[temp_y][temp_x] == 41:
                # when there is an opaque block
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


def block_moves(matrix_copy):

    # create an empty array for open 0 centroids and moveable blocks
    moveable = []

    # parse through rows of grid-matrix that can contain a centroid
    for m in range(1, len(matrix_copy) - 1, 2):
       
        # parse through columns of grid-matrix that can contain a centroid
        for n in range(1, len(matrix_copy[0]) - 1, 2):

            # if grid centroid value belongs to an open block or a moveable block
            if matrix_copy[m][n] == 30 or matrix_copy[m][n] == 40\
                    or matrix_copy[m][n] == 50 or matrix_copy[m][n] == 0:

                # add to moveable array
                moveable.append(matrix_copy[m][n])

            else:
                continue

    # random shuffle array
    random.shuffle(moveable)

    count = 0

    # parse through rows of grid-matrix that can contain a centroid
    for m in range(1, len(matrix_copy) - 1, 2):

        # parse through columns of grid-matrix that can contain a centroid

        for n in range(1, len(matrix_copy[0]) - 1, 2):
            # if we have already added all of the moveable numbers back in, stop loop

            if count == len(moveable):
                break

            # if grid value does not euqal to x block or fixed block
            elif matrix_copy[m][n] != 1 and matrix_copy[m][n] != 31\
                    and matrix_copy[m][n] != 41 and matrix_copy[m][n] != 51:

                # fill new centroid with a value from the shuffled moveable array
                matrix_copy[m][n] = moveable[count]

                # count the number of times this is done so as to not exceed the moveable array
                count = count + 1

            else:
                continue
    # print(matrix_copy)
    return matrix_copy

if __name__ == "__main__":

    grid_matrix, count_reflect, count_opaque, count_refract, L, P = Read_file(
        "mad_1.bff")

    # inserting 20 for the points that we need the laser to intersect
    for i in range(0, len(P)):

        temp_P = P[i]
        xx = temp_P[0]
        yy = temp_P[1]

        grid_matrix[yy][xx] = 20

    matrix_copy = grid_matrix

    make_cross(grid_matrix)

    # Updating the positions of laser start and the points.

    # inserting 10 to laser start points in the matrix grid

    for i in range(0, len(L)):

            temp_L = L[i]
            x = temp_L[0]
            y = temp_L[1]
            vx = temp_L[2]
            vy = temp_L[3]

            grid_matrix[y][x] = 10

            laser_path(y, x, vx, vy, grid_matrix)

    print("going to check if all points hit loop")
    print(grid_matrix)
    print("\n")

    c = 0

    while check_allhit(grid_matrix, P) == False:

        grid_matrix = block_moves(matrix_copy)

        make_cross(grid_matrix)


        # Updating laser path for every new block position
        for i in range(0, len(L)):

            temp_L = L[i]
            x = temp_L[0]
            y = temp_L[1]
            vx = temp_L[2]
            vy = temp_L[3]

            grid_matrix[y][x] = 10

            laser_path(y, x, vx, vy, grid_matrix)

            print(grid_matrix)

            c = c + 1 

        if c == 10:
            break


    print("came out of functions ... all points hit")
    print(grid_matrix)
    print("\n")



    '''
    Test to check if all points hits
    MAKE SURE TO COMMENT WHILE LOOP

    for i in range(0, len(P)):

        temp_P = P[i]
        xx = temp_P[0]
        yy = temp_P[1]

        grid_matrix[yy][xx] = 11


    print(grid_matrix)
    print("\n")


    if check_allhit(grid_matrix, P):
        print("all points hit")
        # print(grid_matrix)
        print("\n")


    else:
        print("not hit")
        # print(grid_matrix)
        print("\n")

    '''
