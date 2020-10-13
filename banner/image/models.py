from django.db import models

from colorfield.fields import ColorField

# Create your models here.
class Side(models.Model):
    name = models.CharField(max_length=100, default='')
    points = models.IntegerField(default=0)
    colour = ColorField(default='#00FF00')
    logo = models.ImageField(upload_to='upload', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, default="")
    side = models.ForeignKey(Side, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-points', 'name']


class BannerConfig(models.Model):
    class Meta:
        verbose_name_plural = "Banner config"

    def __str__(self):
        return "Main config"


class BannerConfigEntry(models.Model):
    config = models.ForeignKey(BannerConfig, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    x1 = models.IntegerField(default=-1)
    y1 = models.IntegerField(default=-1)
    x2 = models.IntegerField(default=-1)
    y2 = models.IntegerField(default=-1)
    size = models.IntegerField(default=-1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Banner config entries"
