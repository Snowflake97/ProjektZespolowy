# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')
#
# import django
#
# django.setup()
#
# from Simulator.Communication import *
#
#
# def run():
#     gameboard = Gameboard()
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
#     # PYTHON INTERPRETER */ProjektZesplowy/venv/bin/python (might change)
#     PYTHON_INTERPRETER_DIR = os.path.join(BASE_DIR, "venv", "bin", "python")
#     # NODEJS INTERPRETER (sudo-apt get install nodejs)
#     NODE_INTERPRETER_DIR = "/usr/bin/nodejs"
#
#     # */Projektespolowy/Simulator/bot.js (will change for sure)
#     BOT_1_DIR = os.path.join(BASE_DIR, "media", "bots", "bot.js")
#     # */Projektespolowy/Simulator/bot.py (will change for sure)
#     BOT_2_DIR = os.path.join(BASE_DIR, "media", "bots", "bot.py")
#
#     # for this to work u should have virtual enviroment in ProjektZespolowy main directiory (same level as ProjektZespolowy, Simulator, tron_app etc)
#     # example: */ProjektZespolowy/venv/bin/python
#     # this might change
#     bot_1 = pexpect.spawn(f"{PYTHON_INTERPRETER_DIR} {BOT_1_DIR} bot_1")  # python bot
#     # bot_2 = pexpect.spawn(f"{PYTHON_INTERPRETER_DIR} {BOT_DIR} bot_2") # python bot
#     bot_2 = pexpect.spawn(f"{NODE_INTERPRETER_DIR} {BOT_2_DIR} bot_2")  # js bot
#     for i in range(20):
#         row, col = whole_seq(bot_1)  # sequence for bot1(get position and direction, send map to bot and mark move)
#         if gameboard.check_if_colision(row, col):
#             print("Colision")
#             break
#         else:
#             gameboard.set_on_position(row, col, 1)  # mark returned position
#
#         row, col = whole_seq(bot_2)  # sequence for bot2(get position and direction, send map to bot and mark move)
#         if gameboard.check_if_colision(row, col):
#             print("Colision")
#             break
#         else:
#             gameboard.set_on_position(row, col, 2)  # mark returned position
#
#     bot_1.close()
#     bot_2.close()
