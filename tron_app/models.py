from django.db import models
from django.utils import timezone
import os


class Matrix(models.Model):
    bot_1 = models.FileField(upload_to='bots/', blank=True)
    bot_2 = models.FileField(upload_to='bots/', blank=True)
    name = models.CharField(max_length=255)
    rows = models.IntegerField(default=0)
    cols = models.IntegerField(default=0)

    def bot_1_name(self):
        return os.path.basename(self.bot_1.name)
    def bot_2_name(self):
        return os.path.basename(self.bot_2.name)

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
