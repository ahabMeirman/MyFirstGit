from django.contrib.auth.models import User
from django.shortcuts import render
from translate.filters import UserFilter

#это пример простого поиска фильтрации пользователей
def search(request):
	user_list = User.objects.all()
	user_filter = UserFilter(request.GET, queryset=user_list)
	return render(request, 'queryset_filter/user_list.html', context = {'filter' : user_filter})