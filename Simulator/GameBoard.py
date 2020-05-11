from tron_app.models import Cell, Matrix
from django.db.models import Max
from django.utils import timezone
from datetime import datetime
import os


class Gameboard:
    def __init__(self):
        self.matrix = Matrix.objects.last()
        self.bot_1 = self.matrix.bot_1_name()
        self.bot_2 = self.matrix.bot_2_name()
        self.rows = self.matrix.cell_set.all().aggregate(Max('row'))['row__max'] + 1  # get row size
        self.columns = self.matrix.cell_set.all().aggregate(Max('col'))['col__max'] + 1  # columns size
        self.game_map = self.load_map()  # load map from db

    def load_map(self):
        game_map = []
        for row in range(self.rows):
            game_map.append([])
            for column in range(self.columns):
                game_map[row].append(self.matrix.cell_set.get(row=row, col=column).val)
        return game_map

    def print_map(self):
        for row in self.game_map:
            print(row)

    def get_value_from_position(self, row: int, column: int):
        return self.game_map[row][column]

    def set_on_position(self, row: int, column: int, obj_to_set):
        if row != None and column != None:
            self.game_map[row][column] = obj_to_set
            cell = self.matrix.cell_set.get(row=row, col=column)  # get cell from db
            cell.val = obj_to_set  # change value
            cell.time = datetime.now(tz=timezone.utc)  # set current time
            cell.save()  # save cell to db

    def check_if_colision(self, row: int, column: int):
        '''
        :param row:
        :param column:
        :return: True if colision, False if correct
        '''
        if row == None and column == None:
            return False
        else:
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
        map_string = ""
        map_len = len(map_piece)
        for rows in map_piece:
            for tups in rows:
                row, col, val = tups
                data = "{}.{}.{}".format(row, col, val)
                map_string += data
                map_string += ":"

        map_string += str(map_len - 1)
        return map_string

    def is_move_possible(self, row, column):

        up = row - 1, column
        down = row + 1, column
        left = row, column - 1
        right = row, column + 1

        surrounding = [up, down, left, right]

        state = False
        for surr in surrounding:
            row, col = surr
            print(surr)
            if row >= 0 and row < self.rows:
                if col >= 0 and col < self.columns:
                    if self.game_map[row][col] == 0:
                        state = True
                        break
        return state

    def change_result(self, result):
        self.matrix.result = result
        self.matrix.save()
