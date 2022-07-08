from django.urls import path
from .views import *
urlpatterns = [
	path('',login_fun,name='insert'),
	path('posts',main_fun,name='posts'),
	path('replay',replay_fun,name='replay') ,
    path('tags',tag_fun,name='tags'),
    path('history',history_fun,name='history'),
    path('notifications',notifications,name='noti'),
    path('search',search_fun,name='search_query'),
    path('sign_up',sign_up_fun,name='sign_up')
]