import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

django.setup()

from Simulator.Communication import *

def spawn_bots(gameboard):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # PYTHON INTERPRETER */ProjektZesplowy/venv/bin/python (might change)
    PYTHON_INTERPRETER_DIR = os.path.join(BASE_DIR, "venv", "bin", "python")
    # NODEJS INTERPRETER (sudo-apt get install nodejs)
    NODE_INTERPRETER_DIR = "/usr/bin/nodejs"

    # */Projektespolowy/media/bots/botname
    BOT_1_DIR = os.path.join(BASE_DIR, "media", "bots", gameboard.bot_1)
    BOT_2_DIR = os.path.join(BASE_DIR, "media", "bots", gameboard.bot_2)

    if (gameboard.bot_1[-2:] == 'py'):
        bot_1 = pexpect.spawn(f"{PYTHON_INTERPRETER_DIR} {BOT_1_DIR} bot_1")
    elif (gameboard.bot_1[-2:] == 'js'):
        bot_1 = pexpect.spawn(f"{NODE_INTERPRETER_DIR} {BOT_1_DIR} bot_1")  #
    else:
        bot_1 = None

    if (gameboard.bot_2[-2:] == 'py'):
        bot_2 = pexpect.spawn(f"{PYTHON_INTERPRETER_DIR} {BOT_2_DIR} bot_2")
    elif (gameboard.bot_1[-2:] == 'js'):
        bot_2 = pexpect.spawn(f"{NODE_INTERPRETER_DIR} {BOT_2_DIR} bot_2")  #
    else:
        bot_2 = None

    return bot_1, bot_2


def run():
    gameboard = Gameboard()
    bot_1, bot_2 = spawn_bots(gameboard)

    if bot_1 != None and bot_2 != None:

        for i in range(20):
            row, col = whole_seq(bot_1)  # sequence for bot1(get position and direction, send map to bot and mark move)
            if gameboard.check_if_colision(row, col):
                print("Colision")
                break
            else:
                gameboard.set_on_position(row, col, 1)  # mark returned position

            row, col = whole_seq(bot_2)  # sequence for bot2(get position and direction, send map to bot and mark move)
            if gameboard.check_if_colision(row, col):
                print("Colision")
                break
            else:
                gameboard.set_on_position(row, col, 2)  # mark returned position

        bot_1.close()
        bot_2.close()

    else:
        # if bots not loaded
        pass