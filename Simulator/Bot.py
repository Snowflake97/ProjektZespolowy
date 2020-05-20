import os
import pexpect
import re
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# PYTHON INTERPRETER */ProjektZesplowy/venv/bin/python (might change)
PYTHON_INTERPRETER_DIR = os.path.join(BASE_DIR, "venv", "bin", "python")

# NODEJS INTERPRETER (sudo-apt get install nodejs)
NODE_INTERPRETER_DIR = "/usr/bin/nodejs"


class Bot:
    def __init__(self, bot_name, id, start_row, start_column):
        self.bot_name = bot_name
        self.bot_mark_value = id
        self.id = "bot"+str(id)
        self.bot = self.spawn_bot()
        self.current_row = start_row
        self.current_column = start_column
        directions = ['left', 'up', 'down', 'right']
        self.current_direction = directions[random.randint(0,3)]

    def spawn_bot(self):
        # */Projektespolowy/media/bots/botname
        BOT_DIR = os.path.join(BASE_DIR, "media", "bots", self.bot_name)

        if (self.bot_name[-2:] == 'py'):
            bot = pexpect.spawn(f"{PYTHON_INTERPRETER_DIR} {BOT_DIR} {self.id}")
        elif (self.bot_name[-2:] == 'js'):
            bot = pexpect.spawn(f"{NODE_INTERPRETER_DIR} {BOT_DIR} {self.id}")  #
        else:
            bot = None

        return bot

    def send_map_piece(self, map_piece_str):
        self.bot.sendline(f"map---{map_piece_str}")
        anwser = self.bot.expect(["MAP_RECEIVED", pexpect.EOF], timeout=5)


    def get_next_move(self):
        self.bot.sendline("move")
        try:
            anwser = self.bot.expect('MOVE---\d+---\d+', timeout=2)
        except:
            return None, None

        #
        next_move_row, next_move_col = self.decode_next_move_from_msg()
        next_move_direction = self.get_move_direction(next_move_row, next_move_col)

        if next_move_direction != 'wrong':
            self.current_row = next_move_row
            self.current_column = next_move_col
            self.current_direction = next_move_direction
            return self.current_row, self.current_column
        else:
            return None, None


    def decode_next_move_from_msg(self):
        msg = self.bot.after.decode("utf-8")
        coordinates = re.findall(r'\d+', msg)

        row = int(coordinates[0])
        col = int(coordinates[1])

        return row, col


    def get_move_direction(self, row, col):
        if row == self.current_row and col == self.current_column - 1:
            move = 'left'
        elif row == self.current_row and col == self.current_column + 1:
            move = 'right'
        elif row == self.current_row - 1 and col == self.current_column:
            move = 'up'
        elif row == self.current_row + 1 and col == self.current_column:
            move = 'down'
        else:
            move = 'wrong'      # when bot wants do wrong move

        return move
