import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

django.setup()

from Simulator.Communication import *
import time, random

gameboard = Gameboard()

bot_1 = pexpect.spawn(f"/home/adi/venv/bin/python bot.py bot_1")
bot_2 = pexpect.spawn(f"/home/adi/venv/bin/python bot.py bot_2")
for i in range(20):
    row, col = whole_seq(bot_1)  # sequence for bot1(get position and direction, send map to bot and mark move)
    if gameboard.check_if_colision(row,col):
        print("Colision")
        break
    else:
        gameboard.set_on_position(row, col, 1)  # mark returned position

    row, col = whole_seq(bot_2)  # sequence for bot2(get position and direction, send map to bot and mark move)
    if gameboard.check_if_colision(row,col):
        print("Colision")
        break
    else:
        gameboard.set_on_position(row, col, 2)  # mark returned position

bot_1.close()
bot_2.close()
