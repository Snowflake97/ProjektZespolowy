import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

django.setup()

from Simulator.GameBoard import Gameboard

gameboard = Gameboard()

# gameboard.set_on_position(11, 10, 1)
# gameboard.set_on_position(10, 10, 1)
# gameboard.print_map()
# print("\n\n")

# print(gameboard.check_if_colision(0,1))
# map_piece = gameboard.get_map_piece((10, 10), "down", 2, 5)
# for row in map_piece:
#     print(row)
#
# print("\n\n")
# map_piece_string = gameboard.convert_map_piece_to_string(map_piece)
#
# map_matrix = gameboard.convert_string_map_piece_to_matrix(map_piece_string)
# for i in map_matrix:
#     print(i)
