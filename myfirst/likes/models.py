from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.db.models import Sum #Возвращает сумму всех значений указанного выражения.
from django.contrib.auth import get_user_model#получаем данные User

User = get_user_model()

class LikeDislikeManager(models.Manager):

	#Django позволяет указать, что созданный вам менеджер должен использоваться как “автоматически созданный менеджер”, 
	#каждый раз когда он добавлен в модель как менеджер по умолчанию. 
	#Это можно сделать, используя атрибут use_for_related_fields:
	use_for_related_fields = True

	#это все связьи операции делается с помощью GenericReletions типа: Blog.votes.likes() ключевое = votes
	def likes(self):
		# Забираем queryset с записями больше 0
		return self.get_queryset().filter(vote__gt=0)

	def dislikes(self):
		# Забираем queryset с записями меньше 0
		return self.get_queryset().filter(vote__lt=0)

	def sum_rating(self):
		# Забираем суммарный рейтинг
		return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class LikeDislike(models.Model):
	LIKE = 1
	DISLIKE = -1

	VOTES = (
		(DISLIKE, 'Не нравится'),
		(LIKE, 'Нравится')
	)

	vote = models.SmallIntegerField(verbose_name = "Голос", choices = VOTES)
	user = models.ForeignKey(User, verbose_name = "Пользователь", on_delete = models.CASCADE)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	objects = LikeDislikeManager()


