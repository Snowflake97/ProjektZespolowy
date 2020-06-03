import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

django.setup()

from Simulator.Bot import Bot
from Simulator.GameBoard import Gameboard
import random

game_on = True
MAP_CREATED_FROM_FILE = False
OBSTACLES = []


def load_obstacle_from_file(file_obstacle_line):
    start_point, end_point = file_obstacle_line.split('-')

    start_row, start_column = start_point.split(',')
    end_row, end_column = end_point.split(',')

    start_row = int(start_row)
    start_column = int(start_column)
    end_row = int(end_row)
    end_column = int(end_column)

    if start_row != end_row and start_column != end_column:
        # not creating straigh line
        return
    elif start_row == end_row and start_column == end_column:
        # creating a point
        OBSTACLES.append((start_row, start_column, 9))

    elif start_row == end_row:
        # horizontal line
        for column in range(start_column, end_column+1):
            OBSTACLES.append((start_row, column, 9))

    elif start_column == end_column:
        for row in range(start_row, end_row + 1):
            OBSTACLES.append((row, start_column, 9))


def load_map_from_file(file):

    with open(file) as f:
        file_lines = f.readlines()

    if len(file_lines) > 1:
        size = file_lines[0].split('x')
        file_obstacles = file_lines[1:]

        for obstacle in file_obstacles:
            load_obstacle_from_file(obstacle)

        return int(size[0]), int(size[1])

    elif len(file_lines) == 1:
        size = file_lines[0].split('x')
        return int(size[0]), int(size[1])
    else:
        return 30, 30


def bot_move(bot, gameboard):
    front_size = int(gameboard.matrix.bot_front_view_size)
    side_size = int(gameboard.matrix.bot_side_view_size)

    map_piece = gameboard.get_map_piece((bot.current_row, bot.current_column), bot.current_direction, front_size, side_size)
    map_piece_str = gameboard.convert_map_piece_to_string(map_piece)

    try:
        bot.send_map_piece(map_piece_str)
    except:
        print(f"Sending map piece to bot {bot.bot_name} unsuccesful")
        return None

    move = bot.get_next_move()

    if move != None:
        row, column = move
        return row, column
    else:
        return None


def get_random_start_position_for_bot(gameboard):
    position_valid = False
    while not position_valid:
        row = random.randint(0, gameboard.rows - 1)
        col = random.randint(0, gameboard.columns - 1)

        for obstacle in OBSTACLES:
            if row == obstacle[0] and col == obstacle[1]:
                continue
            else:
                position_valid = True

        position_valid = True


    OBSTACLES.append((row, col, 9))
    return row, col


def run():
    bot_1_bad_moves_counter = 0
    bot_2_bad_moves_counter = 0
    gameboard = Gameboard()

    if MAP_CREATED_FROM_FILE:
        gameboard.create_obstacles(OBSTACLES)

    bot_1_start_row, bot_1_start_column = get_random_start_position_for_bot(gameboard)
    bot_2_start_row, bot_2_start_column = get_random_start_position_for_bot(gameboard)

    OBSTACLES.pop(-1)
    OBSTACLES.pop(-1)

    bot1 = Bot(gameboard.bot_1, 1, bot_1_start_row, bot_1_start_column)
    bot2 = Bot(gameboard.bot_2, 2, bot_2_start_row, bot_2_start_column)


    if bot1 != None and bot2 != None:
        gameboard.change_result("Game on")

        while True:
            if gameboard.is_move_possible(bot1.current_row,
                                          bot1.current_column) == False and gameboard.is_move_possible(bot2.current_row,
                                                                                                       bot2.current_column) == False:
                gameboard.change_result(result="Tie")
                break
            elif gameboard.is_move_possible(bot1.current_row, bot1.current_column) == False:
                gameboard.change_result(result="Red wins")
                break
            elif gameboard.is_move_possible(bot2.current_row, bot2.current_column) == False:
                gameboard.change_result(result="Blue wins")
                break

            bot_1_move = bot_move(bot1, gameboard)
            bot_2_move = bot_move(bot2, gameboard)

            if bot_1_move == (None, None):
                bot_1_bad_moves_counter += 1
                print(bot_1_bad_moves_counter)
                if(bot_1_bad_moves_counter >5):
                    gameboard.change_result(result="Red wins")

            if bot_2_move == (None, None):
                bot_2_bad_moves_counter += 1
                if(bot_2_bad_moves_counter >5):
                    if (bot_1_bad_moves_counter <= 5):
                        gameboard.change_result(result="Blue wins")
                    else:
                        gameboard.change_result(result="Tie")
                    break

            if bot_1_move == bot_2_move and bot_1_move != (None, None):
                gameboard.change_result(result="Tie")
                break
            elif gameboard.check_if_colision(bot_1_move[0], bot_1_move[1]):
                gameboard.change_result(result="Red wins")
                break
            elif gameboard.check_if_colision(bot_2_move[0], bot_2_move[1]):
                gameboard.change_result(result="Blue wins")
                break
            else:
                gameboard.set_on_position(bot_1_move[0], bot_1_move[1], bot1.bot_mark_value)
                gameboard.set_on_position(bot_2_move[0], bot_2_move[1], bot2.bot_mark_value)
    else:
        gameboard.change_result("There is problem with bots")

    # OBSTACLES.clear()

    bot1.bot.close()
    bot2.bot.close()


if __name__ == "__main__":
    gameboard = Gameboard()
