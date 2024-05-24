from django.contrib.auth.models import AbstractUser
from django.db import models
from my_music.models import AllMusic


class User(AbstractUser):
    myMusic = models.ManyToManyField(AllMusic, blank=True, verbose_name="Music:")
    last_search_query = models.CharField(max_length=40, blank=True)
    music_search_id = models.CharField(max_length=100000, blank=True)
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
