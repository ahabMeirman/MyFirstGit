from django.urls import path
from .views import *

urlpatterns = [
	path('', photo_list, name='photo_list_url'),
]
