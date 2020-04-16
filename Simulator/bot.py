import sys
import time
import random

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
        # print(rows)
        if (len(rows) == rows_size):
            map.append(rows)
            rows = []

    return map


current_row = 15
current_col = 12

while True:
    line = sys.stdin.readline()
    if "move" in line:
        # send next move
        current_row = random.randint(0, 19)
        current_col = random.randint(0, 19)
        print(f"MOVE---{current_row}---{current_col}")
    if "position_and_direction" in line:
        # left or down or up or right
        print(f"ROW---{current_row}---COLUMN---{current_col}---DIRECTION---LEFT")
    if "map" in line:
        # convert string to matrix map
        string_map = line.replace("map---", "")
        matrix_map = convert_string_map_piece_to_matrix(string_map)
        print(f"MAP_RECEIVED")
        # decide next move

    time.sleep(0.01)
