from __future__ import unicode_literals
from django.db import models

from django.db import models

class Neighbourhood(models.Model):

    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class House(models.Model):

    name = models.CharField(max_length=32)
    neighbourhood = models.ForeignKey(Neighbourhood)
    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=32)
    house = models.ForeignKey(House)
    description = models.TextField()

    def __str__(self):
        return self.name


class TestBalkjes(models.Model):
    volume = models.IntegerField()
    def __str__(self):
        return self.volume
