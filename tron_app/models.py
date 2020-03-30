from django.db import models
from django.utils import timezone
import datetime


class Matrix(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Cell(models.Model):
    matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    val = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "row:{}, column:{}".format(self.row, self.col)
