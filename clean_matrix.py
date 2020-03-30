import os

# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektZespolowy.settings')

import django

# Import settings
django.setup()

from tron_app.models import Matrix
import time

def clean():
    matrix = Matrix.objects.last()
    cell_list = matrix.cell_set.filter(val__gte=0)
    for cell in cell_list:
        cell.val = 0
        cell.save()

if __name__ == '__main__':
    start = time.time()
    clean()
    end = time.time() - start
    print("After: {}".format(end))
