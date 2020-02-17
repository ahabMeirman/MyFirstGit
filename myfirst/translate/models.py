from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import LikeDislike

from django.utils import timezone
from django.shortcuts import reverse

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import get_user_model#получаем данные User

User = get_user_model()

# Этот класс преднозначен для дополнительной инфомации в Learn More
#__________________________________________________________
class Articles(models.Model):
	article_title = models.CharField(max_length=200, primary_key=True)
	article_text = models.TextField()
	article_date = models.DateTimeField('date published')

	def __str__(self):
		return self.article_title



# это классы предназначенные для отображения блога с комментариями
# _________________________________________________________
class Blog(models.Model):


	class Meta:
		#для упорядочивания списка постов по дате публикации
		ordering = ['-date']

	title = models.CharField(max_length=100, unique=True)
	text = models.TextField()
	date = models.DateTimeField('date published')

	#ContentType----------------------
	votes = GenericRelation(LikeDislike, related_query_name='count_likes')
	#related_query_name - используется в фильтрах поиска пример: t.objects.filter(count_likes)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('view_blog_detail_url', kwargs={'title': self.title})


#класс комментарии________________________________________
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
	likes_tweet = GenericRelation(LikeDislike, related_query_name='tweeted_likes')

# заглавные посты__________________________________________
class Heading(models.Model):

	title = models.CharField(max_length = 50, unique = True) 
	text = models.TextField(blank = True) 

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('heading_detail_url', kwargs = {'title': self.title})
# c помощью get_absolute_url можно в админке проити на сайт через view on site 


# популярные статьи _______________________________________и админка на нее 
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


# ограничение входа при неправильном пароле________________и админка
class LimitAuthBanIp(models.Model):

	class Meta:
		db_table = "LimitAuthBanIp"

	ip_address = models.GenericIPAddressField("IP адрес")
	attempts = models.IntegerField("Неудачных попыток", default = 0)
	time_unblock = models.DateTimeField("Время разблокировки", blank = True)
	status = models.BooleanField("Статус блокировки", default=False)

	def __str__(self):
		return self.ip_address

class LimitAuthBanIpAdmin(admin.ModelAdmin):

	list_display = ('ip_address', 'status', 'attempts', 'time_unblock')
	search_fields = ('ip_address',)


#Абстрактная модель для системы закладок_____________________________
#Абстрактная модель не можетбыть зарегистрированна в admin.py
#удобны при определении общих, для нескольких моделей, полей
class BookmarkBase(models.Model):

	class Meta:
		abstract = True #Делаем абстрактную модель

	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Пользователь')#Пользователь будет единым для всех моделей закладок

	def __str__(self):
		return self.user.username

#отдельная модель для закладок для статей Blog________________________
class BookmarkBlog(BookmarkBase):#наследуем данные от абстрактной модели

	class Meta:
		db_table = 'bookmark_blog'

	obj = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name = 'Статья')#делаем связь с статьей
	#получаеться у класса BookmarkBlog два поля модели это user, obj
	status_bookmark = models.BooleanField("Статус заметки", default = False)