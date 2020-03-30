from django.urls import path
from . import views

app_name = "tron_app"

urlpatterns = [
    path('', views.index, name="index"),
    path("tron/", views.tron, name="tron"),
    path("tron/clean/", views.clean_board, name="clean"),
    path("tron/run", views.make_moves, name="run"),
    path("tron/lastCells/", views.get_last_cells, name="lastCells")
]
