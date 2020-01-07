from django import forms
from .models import *
from django.core.exceptions import ValidationError

class CommentForm(forms.ModelForm):

	class Meta:
		model = Blog
		fields = ['text']

		widgets = {
			'text' : forms.TextInput(attrs={'class':'form-control'})
		}

#	def save(self):
#		new_comment = Comments.objects.create(text = self.cleaned_data['text'])
#		return new_comment


class HeadingCreateForm(forms.ModelForm):

#	title = forms.CharField(max_length=150)
#	text = forms.CharField()
#
#   Это простое с использованием forms.Form класса представление в шаблоне формы бутстрапа
#	title.widget.attrs.update({'class':'form-control'})
#	text.widget.attrs.update({'class':'form-control'})

# Это более лучше и короткий способ обьявлении форм с помощью Meta
	class Meta:
		 model = Heading
		 fields = ['title','text']

		 widgets = {
		 	'title' : forms.TextInput(attrs={'class':'form-control'}),
		 	'text' : forms.TextInput(attrs={'class':'form-control'})
		 }

	def clean_slug(self):

		new_title = self.cleaned_data['title'].lower()

		if new_title == 'create':
			raise ValidationError('Title may not be "Create"')
		if Heading.objects.filter(title__iexact=new_title).count():
			raise ValidationError('Title "{}" must be unique'.format(new_title))

		return new_title

# Метод save() можно удалить так как в ModelForm есть свой метод сохранения!!
# Этот метод каждый раз создает новый Hefding
# ModelForm можно изменять раннее созданый обьект 
#	def save(self):
#		new_heading = Heading.objects.create(title = self.cleaned_data['title'], text = self.cleaned_data['text'])
#		return new_heading

class SendContactForm(forms.Form):
	

#	class Meta:

#		fields = ['name', 'email', 'message']

#		widgets = {
#			'name' : forms.TextInput(attrs={'class':'form-control'}),
#			'email': forms.EmailInput(attrs={'class':'form-control'}),
#			'message' : forms.Textarea(attrs={'class':'form-control'})
#
#		}


	name = forms.CharField(
		label="Имя",
		widget=forms.TextInput
	)
	
	email = forms.EmailField(
		widget=forms.EmailInput
	)

	message = forms.CharField(
		label="Сообщение",
		widget=forms.Textarea
	)

	name.widget.attrs.update({'class':'form-control'})
	email.widget.attrs.update({'class':'form-control'})
	message.widget.attrs.update({'class':'form-control'})