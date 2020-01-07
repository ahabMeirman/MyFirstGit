from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import *

from django.db.models import Sum
from django.utils import timezone

class ObjectDetailMixinAndComments:

	model = None
	template = None
	form_take = None

	def get(self, request, *args, **kwargs):

		obj = get_object_or_404(self.model, title__iexact = self.kwargs["title"])
		f = self.form_take
		comments_id = obj.id
		return render(request, self.template, context = {self.model.__name__.lower(): obj, 'comments': Comments.objects.filter(reletionships_id=comments_id), 'form': f })

#This is original type function:
#	def get(self, request, title):
#		blog = get_object_or_404(Blog, title__iexact=title)
#		comments_id = blog.id
#		return render(request, 'translate/view_blog_detail.html', context ={'blog': blog, 'comments': Comments.objects.filter(reletionships_id=comments_id)})

class ObjectDaetailViewPostMixin:

	model = None
	template = None
	form_take = None

	def get(self, request, *args, **kwargs):

		obj = get_object_or_404(self.model, title__iexact = self.kwargs["title"])
		f = self.form_take
		comments_id = obj.id
		

#предстовление для отоброжения популяр статей


		obj_key, created = BlogCommonStatistic.objects.get_or_create(defaults = {"blog_key" : obj, "date" : timezone.now()}, date = timezone.now(), blog_key = obj)

		obj_key.views += 1
		obj_key.save(update_fields = ['views'])#Сохроняет только views

		#А теперь забираем список 5 последний самых популярных статей за неделю
		popular = BlogCommonStatistic.objects.filter(date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]).values(
		# Забираем интересующие нас поля, а именно id и заголовок
		# К сожалению забрать объект по внешнему ключу в данном случае не получится
		# Только конкретные поля из объекта
		'blog_key', 'blog_key_id'
		).annotate(
		# Суммируем записи по просмотрам
		# Всё суммируется корректно с соответствием по запрашиваемым полям объектов 
		views=Sum('views')
		).order_by(
		# отсортируем записи по убыванию
		'-views')[:5]  # Заберём последние пять записей

		return render(request, self.template, context = {self.model.__name__.lower(): obj, 'comments': Comments.objects.filter(reletionships_id=comments_id),'form': f, 'popular_list': popular, })