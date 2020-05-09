import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ProjektZespolowy.settings')

import django
# Import settings
django.setup()

from tron_app.models import Cell

def newMatrix(matrix):
    cols = matrix.cols
    rows = matrix.rows

    for i in range(0, rows):
        for j in range(0, cols):
            cell = Cell(row=i, col=j, val=0, matrix=matrix)
            cell.save()

if __name__ == '__main__':
    newMatrix(20,20)
    print('New board created')




