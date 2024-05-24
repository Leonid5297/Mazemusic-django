from django.urls import path
from . import views

urlpatterns = [
    path("", views.MyMusicView.as_view(), name="my_music"),
    path("user/",views.java_script_post, name='js_post'),
    path("search/", views.musicSearch, name='search'),
    path("search/all/", views.java_post_search, name='js_post_search'),
    path("search/add/", views.add_music, name='add_music'),
    path("search/delete/", views.delete_music, name='delete_music'),

]
