from django.db import models


class DoorModel(models.Model):
    name = models.CharField(max_length=50)
    pic = models.ImageField()


