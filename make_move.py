import os

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

# Import settings
django.setup()

from tron_app.models import Cell, Matrix
import time
import datetime
from django.utils import timezone


class Simulation():
    def __init__(self, row, col, my_time):
        self.row = row
        self.col = col
        self.matrix = Matrix.objects.last()
        self.mytime = my_time

    def go_down(self, steps, bot):
        for i in range(steps):
            self.row += 1
            cell = self.matrix.cell_set.get(row=self.row, col=self.col)
            cell.val = bot
            cell.time = datetime.datetime.now(tz=timezone.utc)
            cell.save()
            time.sleep(self.mytime)

    def go_up(self, steps, bot):
        for i in range(steps):
            self.row -= 1
            cell = self.matrix.cell_set.get(row=self.row, col=self.col)
            cell.val = bot
            cell.time = datetime.datetime.now(tz=timezone.utc)
            cell.save()
            time.sleep(self.mytime)

    def go_left(self, steps, bot):
        for i in range(steps):
            self.col -= 1
            cell = self.matrix.cell_set.get(row=self.row, col=self.col)
            cell.val = bot
            cell.time = datetime.datetime.now(tz=timezone.utc)
            cell.save()
            time.sleep(self.mytime)

    def go_right(self, steps, bot):
        for i in range(steps):
            self.col += 1

            # x, y
            cell = self.matrix.cell_set.get(row=self.row, col=self.col)
            cell.val = bot
            cell.time = datetime.datetime.now(tz=timezone.utc)
            cell.save()
            time.sleep(self.mytime)

    def clearMatrix(self):
        for cell in self.matrix.cell_set.filter(val__gte=0):
            cell.val = 0
            cell.save()


if __name__ == '__main__':
    sim = Simulation(0, 0, 0.2)
    # sim.clearMatrix()
    sim.go_down(5, 1)
    sim.go_right(5, 1)
    sim.go_up(5, 1)
    sim.go_left(5, 1)
