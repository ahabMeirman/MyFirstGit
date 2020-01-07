from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import *

from django.utils import timezone
from django.shortcuts import reverse

from django.contrib import admin

# Этот класс преднозначен для дополнительной инфомации в Learn More
class Articles(models.Model):
	article_title = models.CharField(max_length=200, primary_key=True)
	article_text = models.TextField()
	article_date = models.DateTimeField('date published')

	def __str__(self):
		return self.article_title



# это классы предназначенные для отображения блога с комментариями

class Blog(models.Model):


	class Meta:
		#для упорядочивания списка постов по дате публикации
		ordering = ['-date']

	title = models.CharField(max_length=100, unique=True)
	text = models.TextField()
	date = models.DateTimeField('date published')

	like_blog = GenericRelation(Like, related_query_name='count_likes')
	#related_query_name - используется в фильтрах поиска пример: t.objects.filter(count_likes)

  

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('view_blog_detail_url', kwargs={'title': self.title})


class Comments(models.Model):	

	text = models.TextField()
	reletionships= models.ForeignKey('Blog', blank = True, on_delete=models.CASCADE, related_name = 'blogs') #отношение
    #blank_true озночает что присутствие комментария в блоге может быть не обязательным
    #related_name это мостик между отношениями двух моделей

	pub_date = models.DateTimeField('Дата комментария', default=timezone.now)
   	
	
	def __str__(self):
		return 'ID:{}'.format(self.id)

class Tweet(models.Model):

	body = models.CharField(max_length=150)
	likes = GenericRelation(Like, related_query_name='tweetcd_likes')

class Heading(models.Model):

	title = models.CharField(max_length = 50, unique = True) 
	text = models.TextField(blank = True) 

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('heading_detail_url', kwargs = {'title': self.title})
# c помощью get_absolute_url можно в админке проити на сайт через view on site 


class BlogCommonStatistic(models.Model):

	class Meta:
		db_table = "BlogCommonStatistic"

	blog_key = models.ForeignKey(Blog, on_delete=models.CASCADE)
	date = models.DateTimeField('Дата', default = timezone.now)
	views = models.IntegerField('Просмотры', default = 0)

	def __str__(self):
		return self.blog_key.title

class BlogCommonStatisticAdmin(admin.ModelAdmin):

	list_display = ('__str__', 'date', 'views') # отображаемые поля в админке
	search_fields = ('__str__',) # поле, по которому производится поиск
