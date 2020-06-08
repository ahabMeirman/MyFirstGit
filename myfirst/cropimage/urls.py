from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required#декоратор огроничения доступа, здксь не используется @, а просто обьект на который есть огроничение захватывается в кавычки

urlpatterns = [
	path('', login_required(photo_list), name='photo_list_url'),
]
