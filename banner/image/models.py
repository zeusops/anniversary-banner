from django.db import models

from colorfield.fields import ColorField

# Create your models here.
class Side(models.Model):
    name = models.CharField(max_length=100, default='')
    points = models.IntegerField(default=0)
    colour = ColorField(default='#00FF00')
    logo = models.ImageField(upload_to='images', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, default="")
    side = models.ForeignKey(Side, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
