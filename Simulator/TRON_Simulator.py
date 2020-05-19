import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

django.setup()

from Simulator.Bot import Bot
from Simulator.GameBoard import Gameboard
import random

game_on = True


def bot_move(bot, gameboard):
    side_size = int(gameboard.matrix.bot_front_view_size)
    front_size = int(gameboard.matrix.bot_side_view_size)

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


def get_two_random_start_position(gameboard):
    row1 = random.randint(0, gameboard.rows - 1)
    row2 = random.randint(0, gameboard.rows - 1)
    col1 = random.randint(0, gameboard.columns - 1)
    col2 = random.randint(0, gameboard.columns - 1)
    while row1 == row2 and col1 == col2:
        row1 = random.randint(0, gameboard.rows - 1)
        row2 = random.randint(0, gameboard.rows - 1)
        col1 = random.randint(0, gameboard.columns - 1)
        col2 = random.randint(0, gameboard.columns - 1)
    return row1, col1, row2, col2


def run():
    bot_1_bad_moves_counter = 0
    bot_2_bad_moves_counter = 0
    gameboard = Gameboard()

    bot_1_start_row, bot_1_start_column, bot_2_start_row, bot_2_start_column = get_two_random_start_position(gameboard)
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

    bot1.bot.close()
    bot2.bot.close()


if __name__ == "__main__":
    gameboard = Gameboard()
