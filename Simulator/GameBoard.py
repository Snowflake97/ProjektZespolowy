class Gameboard:
    def __init__(self, size: int):
        self.game_map = []
        self.size = size

        for row in range(self.size):
            self.game_map.append([])
            for column in range(self.size):
                self.game_map[row].append((row, column))

    def print_map(self):
        for row in self.game_map:
            print(row)

    def get_position(self, row: int, column: int):
        return self.game_map[row][column]

    def set_on_position(self, row: int, column: int, obj_to_set):
        self.game_map[row][column] = obj_to_set
