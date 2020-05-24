from django.db import models


class Photo(models.Model):
	file = models.ImageField()
	description = models.CharField(max_length=255, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'photo' #Отображаемое имя поля.
		verbose_name_plural = 'photos'

