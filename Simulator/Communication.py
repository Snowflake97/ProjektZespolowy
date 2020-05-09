# import pexpect
# import re
# from Simulator.GameBoard import Gameboard
# import time
#
# gameboard = Gameboard()
#
#
# def get_next_move(bot):
#     bot.sendline("move")
#     anwser = bot.expect(['MOVE---\d+---\d+'])
#     next_move = bot.after.decode("utf-8")
#     digits = re.findall(r'\d+', next_move)
#     row = int(digits[0])
#     col = int(digits[1])
#
#     position = (row, col)
#
#     return position
#
#
# def get_current_position_and_direction(bot):
#     bot.sendline("position_and_direction")
#     anwser = bot.expect(["ROW---\d+---COLUMN---\d+---DIRECTION---\w+"])
#     data = bot.after.decode("utf-8")
#     elements = data.split("---")
#     current_row = int(elements[1])
#     current_column = int(elements[3])
#     current_direction = elements[5].lower()
#
#     # print(f"{current_row}, {current_column}, {current_direction}")
#     return (current_row, current_column, current_direction)
#
#
# def send_map_piece(bot):
#     row, col, direction = get_current_position_and_direction(bot)
#     map_piece = gameboard.get_map_piece((row, col), direction, 2, 5)
#     map_string = gameboard.convert_map_piece_to_string(map_piece)
#     bot.sendline(f"map---{map_string}")
#     anwser = bot.expect("MAP_RECEIVED")
#     # print("SUCCESS")
#
#
# def whole_seq(bot):
#     send_map_piece(bot)
#     row, col = get_next_move(bot)
#     return (row, col)
