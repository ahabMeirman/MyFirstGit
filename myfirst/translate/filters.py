from django import forms
from django.contrib.auth.models import User, Group # импортируем группы
import django_filters

# класс преднозначен для фильтрации пользователей и поиска
class UserFilter(django_filters.FilterSet):
	first_name = django_filters.CharFilter(lookup_expr = 'icontains')
			# здесь была все время ошибка в атрибутах name='date_joined'
			#ошибка исчезла после того как я поменял на field_name='date_joined'
			#думаю это из за версии
	year_joined = django_filters.NumberFilter(field_name='date_joined', lookup_expr='year')
	groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'groups']