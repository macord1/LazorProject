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

    print(P)


if __name__ == "__main__":
    Read_file("mad_1.bff")
