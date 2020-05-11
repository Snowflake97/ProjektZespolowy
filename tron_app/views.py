from django.shortcuts import render
from make_move import Simulation
from clean_matrix import clean as cleanMatrix
from .models import Matrix, Cell
from django.http import Http404, HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from new_board import newMatrix
from Simulator import TRON_Simulator



def index(request):
    return render(request, "tron_app/index.html")


def tron(request):
    last_matrix = Matrix.objects.last()
    my_dict = {"matrix": last_matrix}

    return render(request, "tron_app/tron.html", context=my_dict)


def clean_board(request):
    if request.is_ajax():
        cleanMatrix()
        more_data = ["finish"]
        data = json.dumps(more_data)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404



def get_last_cells(request):
    last = Matrix.objects.last().cell_set.all().order_by('-time')[:10]
    result = Matrix.objects.last().result
    queryset = last.values("row", "col", "val")
    return JsonResponse({"models_to_return": list(queryset),
                         'result' : result})


def run_simulation(request):
    if request.is_ajax():
        matrix = Matrix.objects.last()
        matrix.result = "Loading bots"
        matrix.save()
        TRON_Simulator.run()
        more_data = ["finish"]
        data = json.dumps(more_data)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404


def prepare_game(request):

    if request.method == 'POST':
        name = request.POST.get('matrix_name')
        bot1 = request.FILES.get('bot1')
        bot2 = request.FILES.get('bot2')
        rows = int(request.POST.get('rows'))
        cols = int(request.POST.get('cols'))

        matrix = Matrix(name=name,bot_1=bot1, bot_2=bot2, rows=rows, cols=cols)
        matrix.save()
        newMatrix(matrix)
        return HttpResponseRedirect('/tron/')
    return render(request, 'tron_app/prepare_game.html')