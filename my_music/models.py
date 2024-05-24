from django.db import models


# Create your models here.
class AllMusic(models.Model):
    name = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=50, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    file = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.author} - {self.name}'


