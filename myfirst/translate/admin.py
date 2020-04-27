from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget#загрузка изоброжении
from django import forms

# Blog и все его настройки в админ панели, плюс виджет который отвечает за отоброжение 
#всех имеющихся инструментов плагина CKEditor________________________________________
class BlogAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'

class BlogAdmin(admin.ModelAdmin):

	list_display = ('title', 'text', 'date',)
	search_fields = ('__str__',)
	form = BlogAdminForm

#регистрация__________________________________________________________________________
admin.site.register(Articles)
admin.site.register(Heading)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comments)
admin.site.register(BlogCommonStatistic, BlogCommonStatisticAdmin)
admin.site.register(LimitAuthBanIp, LimitAuthBanIpAdmin)
admin.site.register(BookmarkBlog)
admin.site.register(UserProfile)#дополнительное рассширение Пользователя(age, location, mail)
admin.site.register(Photo)#Загрузка мультифайлов(несколько) с помощью Ajax