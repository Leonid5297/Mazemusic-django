import json
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from my_music.models import AllMusic
from users.models import User


def java_script_post(request):
    music_user = request.user.myMusic.all()
    data = []
    number = 1
    for music in music_user:
        track = {
            "track": number,
            "name": f'{music.name} - {music.author}',
            "duration": music.duration,
            "file": music.file
        }
        number += 1
        data.append(track)
    if len(data) == 0:
        data.append({
            "track": "Nothing was found for your query.",
            "name": "",
            "duration": '',
            "file": ''
        })
    data = json.dumps(data)
    return HttpResponse(data)


class MyMusicView(View):
    def get(self, request):
        return render(request, 'my_music/index.html')

    def post(self, request):
        return render(request, 'my_music/my_music.html', context={})


def musicSearch(request):
    user = (User.objects.filter(id=request.user.id)).update(last_search_query=request.GET['q'])
    return render(request, 'my_music/search.html')


def java_post_search(request):
    query = request.user.last_search_query
    query_list = query.split()
    all_music = AllMusic.objects
    object_list_1 = []
    object_list_2 = []
    object_list_3 = []

    for query1 in query_list:
        object_list_1 = all_music.filter(
            Q(author__icontains=query1)  # поиск треков автора в query
        )
        if len(object_list_1) > 0:
            break

    if len(object_list_1) > 0:
        current_musics = object_list_1
        for query2 in query_list:
            object_list_1 = current_musics.filter(
                Q(name__icontains=query2)  # поиск трека по названию в новом query
            )
            if len(object_list_1) > 0:
                break  # Найден трек по автору и названию
            object_list_1 = current_musics
    else:  # автор не был передан
        for query1 in query_list:
            object_list_1 = all_music.filter(
                Q(name__icontains=query1)  # поиск треков по названию
            )
            if len(object_list_1) > 0:
                break

    objects = [object_list_1]
    data = []
    number = 1
    id_music = ''
    for music_user in objects:
        for music in music_user:
            track = {
                "track": number,
                "name": f'{music.name} - {music.author}',
                "duration": music.duration,
                "file": music.file
            }
            number += 1
            data.append(track)
            id_music += str(music.id) + "-"
    if len(id_music)>0:
        id_music = id_music[:-1]
    if len(data) == 0:
        data.append({
            "track": "Nothing was found for your query.",
            "name": "",
            "duration": '',
            "file": ''
        })
    data = json.dumps(data)
    user = (User.objects.filter(id=request.user.id)).update(music_search_id=id_music)
    return HttpResponse(data)


def delete_music(request):
    if request.method == 'POST':
        number = request.POST.get("number")
        user = (User.objects.filter(id=request.user.id))[0]
        if number[0] == '0':
            number = number[1:]
        number = int(number) - 1
        try:
            music = user.myMusic.all()[number]
            user.myMusic.remove(music)
            return render(request, 'my_music/index.html', context={'to_add_flag': 'True'})

        except Exception:
            return render(request, 'my_music/index.html', context={'to_add_flag': 'False'})







def add_music(request):
    if request.method == 'POST':
        number = request.POST.get("number")
        if number[0] == '0':
            number = number[1:]
        number = int(number) - 1
        id_music = request.user.music_search_id.split('-')
        try:
            id_music_new = int(id_music[number])
            music = AllMusic.objects.get(id=id_music_new)
        except Exception:
            return render(request, 'my_music/search.html', context={'to_add_flag': 'False'})

        try:
            user = (User.objects.filter(id=request.user.id))[0]
            if music in user.myMusic.all():
                raise Exception
            user.myMusic.add(music)
            return render(request, 'my_music/search.html', context={'to_add_flag': 'True'})
        except Exception:
            return render(request, 'my_music/search.html', context={'to_add_flag': 'False'})

    else:
        return render(request, 'my_music/search.html')

