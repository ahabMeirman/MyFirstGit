from django import template
from translate.models import *
from django.conf import settings
#Кастомные теги

register = template.Library()

@register.simple_tag
def get_attribute(name):
	return getattr(settings, name, "")#функция преднозначенная для передачи атрибута
	# в качестве атрибута у нас "name" a пустая строка - default значение