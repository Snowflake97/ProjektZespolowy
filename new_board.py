import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ProjektZespolowy.settings')

import django
# Import settings
django.setup()

from tron_app.models import Cell, Matrix

def newMatrix(size):

    Matrix.objects.all().delete()
    new_matrix = Matrix(name="test_matrix", cols=size, rows=size)
    new_matrix.save()

    for i in range(0, size):
        for j in range(0, size):
            cell = Cell(row=i, col=j, val=0, matrix=new_matrix)
            cell.save()

if __name__ == '__main__':
    newMatrix(20)
    print('New board created')



