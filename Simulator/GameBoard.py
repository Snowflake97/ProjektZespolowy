from tron_app.models import Cell
from django.db.models import Max
from django.utils import timezone
from datetime import datetime


class Gameboard:
    def __init__(self):
        self.rows = Cell.objects.all().aggregate(Max('row'))['row__max'] + 1  # get row size
        self.columns = Cell.objects.all().aggregate(Max('col'))['col__max'] + 1  # columns size
        self.game_map = self.load_map()  # load map from db

    def load_map(self):
        game_map = []
        for row in range(self.rows):
            game_map.append([])
            for column in range(self.columns):
                game_map[row].append(Cell.objects.get(row=row, col=column).val)
        return game_map

    def print_map(self):
        for row in self.game_map:
            print(row)

    def get_value_from_position(self, row: int, column: int):
        return self.game_map[row][column]

    def set_on_position(self, row: int, column: int, obj_to_set):
        self.game_map[row][column] = obj_to_set
        cell = Cell.objects.get(row=row, col=column)  # get cell from db
        cell.val = obj_to_set  # change value
        cell.time = datetime.now(tz=timezone.utc)  # set current time
        cell.save()  # save cell to db

    def check_if_colision(self, row: int, column: int):
        '''
        :param row:
        :param column:
        :return: True if colision, False if correct
        '''
        if row >= self.rows or row < 0 or column >= self.columns or column < 0 or self.get_value_from_position(row,
                                                                                                               column) != 0:
            return True
        else:
            return False

    def get_map_piece(self, bot_position: tuple, bot_direction: str, side_size: int, front_size: int):
        bot_row, bot_column = bot_position
        map_piece = []
        if bot_direction == "up":
            start_row = bot_row - front_size
            start_col = bot_column - side_size
            current_col = start_col
            current_row = start_row
            for front in range(front_size + 1):
                part_piece = []
                for side in range(2 * side_size + 1):
                    if current_row < 0 or current_row >= self.rows or current_col < 0 or current_col >= self.columns:
                        position = (current_row, current_col, 9)  # mark map end
                    else:
                        position = (current_row, current_col, self.get_value_from_position(current_row, current_col))
                        # position = "{},{}".format(start_row,current_col)
                    part_piece.append(position)
                    current_col += 1
                current_row += 1
                current_col = start_col
                map_piece.append(part_piece)

        elif bot_direction == "down":
            start_row = bot_row + front_size
            start_col = bot_column - side_size
            current_col = start_col
            current_row = start_row
            for front in range(front_size + 1):
                part_piece = []
                for side in range(2 * side_size + 1):
                    if current_row < 0 or current_row >= self.rows or current_col < 0 or current_col >= self.columns:
                        position = (current_row, current_col, 9)  # mark map end
                    else:
                        position = (current_row, current_col, self.get_value_from_position(current_row, current_col))
                    part_piece.append(position)
                    current_col += 1
                current_row -= 1
                current_col = start_col
                map_piece.append(part_piece[::-1])

        elif bot_direction == "left":
            start_row = bot_row + side_size
            start_col = bot_column - front_size

            current_col = start_col
            current_row = start_row

            for front in range(front_size + 1):
                part_piece = []
                for side in range(2 * side_size + 1):
                    if current_row < 0 or current_row >= self.rows or current_col < 0 or current_col >= self.columns:
                        position = (current_row, current_col, 9)  # mark map end
                    else:
                        position = (current_row, current_col, self.get_value_from_position(current_row, current_col))
                    current_row -= 1
                    part_piece.append(position)

                current_col += 1
                current_row = start_row
                map_piece.append(part_piece)

        elif bot_direction == "right":
            start_row = bot_row - side_size
            start_col = bot_column + front_size

            current_col = start_col
            current_row = start_row

            for front in range(front_size + 1):
                part_piece = []
                for side in range(2 * side_size + 1):
                    if current_row < 0 or current_row >= self.rows or current_col < 0 or current_col >= self.columns:
                        position = (current_row, current_col, 9)  # mark map end
                    else:
                        position = (current_row, current_col, self.get_value_from_position(current_row, current_col))
                    current_row += 1
                    part_piece.append(position)

                current_col -= 1
                current_row = start_row
                map_piece.append(part_piece)

        return map_piece

    def convert_map_piece_to_string(self, map_piece: list):
        # conversion from matrix to string
        map_piece_string = ""
        for rows in map_piece:
            for tuples in rows:
                row, column, value = tuples
                data = "{}.{}.{}".format(row, column, value)
                if tuples != rows[-1]:
                    data += ":"
                map_piece_string += data
                map_piece_string.join(":")
            if rows != map_piece[-1]:
                map_piece_string += "-"

        return map_piece_string

    def convert_string_map_piece_to_matrix(self, map_piece: str):
        # conversion from string to matrix
        # decompilation for BOTs
        map = []
        rows = []
        rows_str = map_piece.split("-")
        for row_str in rows_str:
            columns = row_str.split(":")
            for data in columns:
                row, column, value = data.split(".")
                rows.append((int(row), int(column), int(value)))
            map.append(rows)
            rows = []

        return map
