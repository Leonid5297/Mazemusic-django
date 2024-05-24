from django.contrib import admin

# Register your models here.

from .models import AllMusic


class AllMusicAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'duration']


admin.site.register(AllMusic, AllMusicAdmin)
