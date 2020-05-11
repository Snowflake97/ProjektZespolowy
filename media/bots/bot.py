import sys
import time

NAME = sys.argv[1]


def convert_string_map_piece_to_matrix(map_piece: str):
    elements = map_piece.split(":")
    rows_size = elements.pop()
    rows = []
    map = []
    for e in elements:
        row, col, val = e.split(".")
        row = int(row)
        col = int(col)
        val = int(val)
        tup = (row, col, val)
        rows.append(tup)
        if (len(rows) == int(rows_size)):
            map.append(rows)
            rows = []


    return map


current_row = 15
current_col = 12
current_direction = "left"
matrix_map = []

while True:
    line = sys.stdin.readline()
    if "move" in line:
        # send next move
        print(f"MOVE---{current_row}---{current_col}")
    if "position_and_direction" in line:
        # left or down or up or right
        print(f"ROW---{current_row}---COLUMN---{current_col}---DIRECTION---{current_direction}")
    if "map" in line:
        # convert string to matrix map
        print(f"MAP_RECEIVED")
        string_map = line.replace("map---", "")
        matrix_map = convert_string_map_piece_to_matrix(string_map)

        # decide next move
        middle = len(matrix_map[0]) // 2
        left = (len(matrix_map[0]) // 2) - 1
        right = (len(matrix_map[0]) // 2) + 1

        if matrix_map[-2][middle][2] == 0:
            current_row, current_col, _ = matrix_map[-2][middle]
        elif matrix_map[-1][right][2] == 0:
            current_row, current_col, _ = matrix_map[-1][right]
        elif matrix_map[-1][left][2] == 0:
            current_row, current_col, _ = matrix_map[-1][left]
        else:
            pass


    time.sleep(0.01)
