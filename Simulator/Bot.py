import os
import pexpect
import re
import random

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
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # PYTHON INTERPRETER */ProjektZesplowy/venv/bin/python (might change)
        PYTHON_INTERPRETER_DIR = os.path.join(BASE_DIR, "venv", "bin", "python")
        # NODEJS INTERPRETER (sudo-apt get install nodejs)
        NODE_INTERPRETER_DIR = "/usr/bin/nodejs"

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
        anwser = self.bot.expect("MAP_RECEIVED")
        # print("SUCCESS")

    def get_next_move(self):
        self.bot.sendline("move")
        anwser = self.bot.expect(['MOVE---\d+---\d+'])
        next_move = self.bot.after.decode("utf-8")
        digits = re.findall(r'\d+', next_move)
        row = int(digits[0])
        col = int(digits[1])

        if row == self.current_row and col == self.current_column - 1:
            direction = 'left'
        elif row == self.current_row and col == self.current_column + 1:
            direction = 'right'
        elif row == self.current_row - 1 and col == self.current_column:
            direction = 'up'
        elif row == self.current_row + 1 and col == self.current_column:
            direction = 'down'
        else:
            direction = 'wrong'  # when bot wants do wrong move

        if direction != 'wrong':
            self.current_row = row
            self.current_column = col
            self.current_direction = direction
            return self.current_row, self.current_column
        else:
            return None, None
