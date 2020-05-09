from django.shortcuts import render
from make_move import Simulation
from clean_matrix import clean as cleanMatrix
from .models import Matrix, Cell
from django.http import Http404, HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from new_board import newMatrix



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


def make_moves(request):
    if request.is_ajax():
        sim = Simulation(1, 1, 0.2)
        sim.go_down(5, 1)
        sim.go_right(5, 1)
        sim.go_up(5, 1)
        sim.go_left(5, 1)
        more_data = ["finish"]
        data = json.dumps(more_data)
        return HttpResponse(data, content_type="application/json")
    else:
        raise Http404


def get_last_cells(request):
    last = Cell.objects.all().order_by('-time')[:10]
    queryset = last.values("row", "col", "val")
    return JsonResponse({"models_to_return": list(queryset)})


def run_simulation(request):
    if request.is_ajax():
        # run()
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