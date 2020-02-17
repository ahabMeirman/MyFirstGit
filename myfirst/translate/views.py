from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
#это пакеты аутентификации
from django.contrib.auth.forms import AuthenticationForm
from urllib.parse import urlparse#разделяет наш полученный адрес по полычкам
from .special_func import * # мои специальные функциию, описание внутри пакета
from django.contrib.auth import logout# это выход, готовая функция
from django.contrib import messages # success, info, warning, error, debug mehagess
from django.contrib.auth.decorators import login_required#декоратор огроничения доступа
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin# это такойже декоратор как - login_required, только работает с классами
from django.contrib import auth
from django.contrib.auth import get_user_model#получаем данные User
#это пакет готовый набор новый регистрации пользователя
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from .models import *
from .forms import *
from django.views.generic import View
from translate.utils import *

from django.db.models import Q

from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from likes.models import LikeDislike#Это ContentType

from django.views.decorators.http import require_http_methods

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail#отправка сообщении через почту
from django.core import mail

from myfirst import settings
#Этот процессор добавляет токен, который используется тегом csrf_token для защиты от CSRF атак.
from django.template.context_processors import csrf

from django.utils import timezone
import datetime

from django.template.loader import render_to_string
from django.utils.html import strip_tags

#это пакеты системы закладок
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template

#User = get_user_model()
#user = User.objects.get(username)

#def Base(request):
#	headings = Heading.objects.all()
#	return render(request, 'translate/first_list.html', context = {'headings': headings})

#@login_required = этот декоратор используеться только в функциях
def FirstList(request):
	headings = Heading.objects.all()
	return render(request, 'translate/first_list.html', context = {'headings': headings})

#def ViewHeadingDetail(request, title):

#	heading = Heading.objects.get(title__iexact = title)
#	return render(request, 'translate/view_heading_detail.html', context = {'heading': heading})

class ViewHeadingDetail(ObjectDetailMixinAndComments, View):

	model = Heading
	template = 'translate/view_heading_detail.html'


#	def get(self, request, title):

#		heading = get_object_or_404(Heading, title__iexact = title)
#		return render(request, 'translate/view_heading_detail.html', context = {'heading': heading})
class HeadingCreate(LoginRequiredMixin, View):
	
	def get(self, request):
		form = HeadingCreateForm()
		return render(request, 'translate/heading_create.html', context = {'form': form})

	def post(self,request):
		
		bound_form = HeadingCreateForm(request.POST)

		if bound_form.is_valid():
			new_title = bound_form.save()
			return redirect(new_title)		
# Я думаю что redirect связан как то с get_absolute_url потому что он находит путь через экземпляр класса 
		
		return render(request, 'translate/heading_create.html', context = {'form': bound_form})


#class CommentCreate(View):
#
#	def get(self, request):
#		form_comment = CommentForm()
#		return render(request, 'translate/comments_create.html', context = {'form_comment': form_comment})


def LearnMore(request):
	article=Articles.objects.get()
	return render(request, 'translate/learn_more.html', context={'article': article})

#Главная страница блога
def Post(request):



	
#	search_query = request.GET.get('search', '')

#	if search_query:
#		blogs = Blog.objects.filter(Q(title__icontains = search_query) | Q(text__icontains = search_query))
#	
#	else:
#		blogs = Blog.objects.all()

# ___________________PAGINATOR______________________________________
	blogs = Blog.objects.all()
	paginator = Paginator(blogs, 1)
	page_number = request.GET.get('page', 1) #в методе GET в обьекте request в ключе page находится адрес страницы ?page=, 1 это по умолчанию 1 страница
	page = paginator.page(page_number)

	is_paginated = page.has_other_pages() # возвращает True or False если вообщем есть список постов

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''

	context = {
		'blogs' : page,
		'is_paginated' : is_paginated,
		'next_url' : next_url,
		'prev_url' : prev_url,
 	}

	return render(request, 'translate/blog.html', context = context)

#def ViewBlogDetail(request, title):

	#User = get_user_model()
	#user = User.objects.get(id=1)
	#blog = Blog.objects.filter(title__icontains=title)
	#like = Like.objects.create(content_type=ContentType.objects.get_for_model(blog), object_id=blog.id, user=user)
	#like = Like.objects.create(content_object=blog, like_number = 1, user = user)
	#like.save()
	#like.like_number+=1
	#b=like.like_number
		



#	blog = Blog.objects.get(title__iexact=title)
#	comments_id = blog.id
#	return render(request, 'translate/view_blog_detail.html', context ={'blog': blog, 'comments': Comments.objects.filter(reletionships_id=comments_id)})

class ViewBlogDetail(ObjectDaetailViewPostMixin, View):

	model = Blog
	template = 'translate/view_blog_detail.html'
	form_take = CommentForm

	#общая модель выстовляется в url
	modelbookmark = None #так как представление универсальное, то создаем общую модель подстовляя в нее модель закладок типа- BookmarkBlog

#	@require_http_methods(["POST"])
#	def add_comment(request, title):
	

	def post(self, request, *args, **kwargs):
		#если пользаватель авторизован то можно остовлять комментарии
		if auth.get_user(request).is_authenticated:

			form_comment = CommentForm(request.POST)
		
			blog_com = get_object_or_404(Blog, title__iexact = self.kwargs['title'])

			if form_comment.is_valid():
				comment_instanse = Comments()
				comment_instanse.reletionships = blog_com
				comment_instanse.text = form_comment.cleaned_data['text']
				comment_instanse.pub_date = datetime.datetime.now()
				comment_instanse.save()
				return redirect(blog_com)

			return render(request, self.template, context = {'form': form_comment})
		else:
			#если нет то отоброжаем поля регистрации
			
			return redirect('/accounts/login/')#это  готовая аутентификация, я ее выключил пока работает своя написанная аутен
	

'''
def addLike(request, article_id):
	try:
		likes_set = Blog.objects.get(id = article_id)
		likes_set.likes += 1
		likes_set.save()
	except ObjectDoesNotExist:
		raise Http404
	return redirect('first_list_url')
'''

class SendContact(View):

	template = 'translate/send_contact.html'

	def get(self, request):
		# В случае get запроса, мы будем отправлять просто страницу с контактной формой
		context = {}
		context.update(csrf(request))
		context['contact_form_empty'] = SendContactForm()
		return render(request, self.template, context=context)

	def post(self, request):
		context = {}
		form_contact_full = SendContactForm(request.POST)

		if form_contact_full.is_valid():
			email_subject = 'THis is message '
			email_body = 'Thsi is a new \n\n' \
						 'New User:: %s \n' \
						 'E-mail sender: %s \n\n'\
						 'Message: \n'\
						 '%s' %\
						 (form_contact_full.cleaned_data['name'], form_contact_full.cleaned_data['email'], form_contact_full.cleaned_data['message'])

# и отправляем сообщение
			send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['meirman_ahab_90@mail.ru'], fail_silently = False)
		return render(request, self.template, context=context)

#Блокировка злоумышленников по IP при попытках подбора пароля на Django
#_______________________________________________________________________________________
#class LoginView(SuccessURLAllowedHostsMixin, django.views.generic.edit.FormView):
class MyLoginView(View):

	
	def get(self, request):
			

			if auth.get_user(request).is_authenticated:
				#замечание здесь нету токена!!!!!!!!!!
				print('сработал get')
				#здесь я вывожу имя пользователя с помощью messages
				User = auth.get_user(request)
				messages.success(request, "Welkome %s!" % User)

				new_next = url_cut(request)# моя готовая функция смотри описание в special_func.py
				return redirect(new_next)#переходим на тот адрес где мы изночально были до аутентификации
			else:
				context = create_context_username_csrf(request) #загоняем готовую фунцию токен и формы
				return render_to_response('regist/log_widget.html', context=context)
				
	def post(self, request, *args, **kwargs):

		# получив запрос на авторизацию
		form = AuthenticationForm(request, data=request.POST)

		ip = get_client_ip(request)#получаем ip
		#создаем и получаем данные с нашего ip блокиратора, по дефолту даем начальные значения
		obj, created = LimitAuthBanIp.objects.get_or_create(
			defaults = {
				'ip_address' : ip,
				'time_unblock' : timezone.now()
			},
			ip_address = ip
		)
		print('attempts = %s' % obj.attempts)


		if obj.status is True and obj.time_unblock > timezone.now():#пока этот статус не будет false, пользователь не войдет в систему даже с правильным паролем
			if obj.attempts == 3 or obj.attempts == 6:
				return render_to_response('registration/block_15_minutes.html')
			elif obj.attempts == 9:
				return render(request, 'registration/block_24_hours.html')
		elif obj.status is True and obj.time_unblock < timezone.now():
			obj.status = False
			obj.save()

		
        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
		if form.is_valid():

			obj.delete()# данные валидные, удоляем данные с нашего блокиратора
			
            # в случае успеха авторизуем пользователя
			auth.login(request, form.get_user())
			# получаем предыдущий url
			next = urlparse(get_next_url(request)).path
			new_next = url_cut(request)# моя готовая функция смотри описание в special_func.py

			# и если пользователь из числа персонала и заходил через url /admin/login/
			# то перенаправляем пользователя в админ панель
			if new_next == '/admin/log/' and request.user.is_staff:
			    return redirect('/admin/')
			# иначе делаем редирект на предыдущую страницу,
			# в случае с /accounts/login/ произойдёт ещё один редирект на главную страницу
			# в случае любого другого url, пользователь вернётся на данный url
			elif new_next == '/translate/signup/':
				return redirect ('/translate/')
			return redirect(next)

		else:

			obj.attempts += 1
			if obj.attempts == 3 or obj.attempts == 6:
				obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
				obj.status = True
			elif obj.attempts == 9:
				obj.time_unblock = timezone.now() + timezone.timedelta(1)
				obj.status = True
			elif obj.attempts > 9:
				obj.attempts = 1
			obj.save()



		# если данные не верны, то пользователь окажется на странице авторизации
		# и увидит сообщение об ошибке
		context = create_context_username_csrf(request)
		context['form'] = form
		return render_to_response('regist/log_widget.html', context=context)


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
	context = {} #создаем пустой контекст	
	context.update(csrf(request)) #впихиваем в контекст токен
	context['form'] = AuthenticationForm #добовляем пустые формы аутентификации
	return context

#выход пользователя_________________________________________________________
def myLogout(request):
	logout(request)
	print('здесь наша функция')
	next = request.META.get('HTTP_REFERER')#с помощью этого метода получаем полностью url адрес например:'http://127.0.0.1:5000/translate/log/translate/''
	new_next = urlparse(next).query
	new_next = new_next[5:]
	messages.info(request, "Logged out successfully!")#message с использованием шаблона
	#return redirect(new_next)
	return redirect('/translate/')

#закладки____________________________________________________________________
class BookmarkView(View):
	
	modelbookmark = None #так как представление универсальное, то создаем общую модель подстовляя в нее модель закладок типа- BookmarkBlog
	

	def post(self, request, title):#выборка по id
		bookmark_id = Blog.objects.get(title = title).id#получаем статью
		user = auth.get_user(request)#получаем пользователя

		#создаем закладку
		bookmark, created = self.modelbookmark.objects.get_or_create(user = user, obj_id = bookmark_id)#получаем закладку или заново создаем
		
		#используем переменную valid в шаблоне, она у нас стоит в ajax-e
		#конечно код громоздки но пока не придумал, count - это подсчет общего количество закладок или пользователей на опреденную статью
		if created:
			data = {'valid' : True, 'count' : self.modelbookmark.objects.filter(obj_id = bookmark_id).count()}
		else:
			bookmark.delete()#если запроса не было на создание, то запрос на удоление закладку
			data = {'valid' : False, 'count' : self.modelbookmark.objects.filter(obj_id = bookmark_id).count()}

	
		print(request.path)#хороший метод для определения полного url
		print('ajax')
	
		return JsonResponse(data)# в виде строки передается в ajax в - function(data)

#регистрация пользователя с использованием ajax для проверки существующего пользователя
#_reCAPTCHA____________________________________________________________________________
class SignUpView(CreateView):
	template_name = 'regist/signup.html'
	form_class = UserCreationForm

	def form_valid(self, form):
		# проверка валидности reCAPTCHA
		if self.request.recaptcha_is_valid:
			form.save()
			messages.success(self.request, 'Your password was created successfully!')
			return render(self.request, 'regist/signup_success.html', self.get_context_data())
		messages.warning(self.request, 'You need repeat again')
		return render(self.request, 'regist/signup.html', self.get_context_data())

# функция для проверки существующего имени пользователя	
def validate_username(request):
	username = request.GET.get('username', '')#получаем от inputa данные

	data = {
		'is_taken': User.objects.filter(username__iexact = username).exists()#с помощью фильтра проверяем есть ли такой пользователь в базе
	}
	return JsonResponse(data)#с помощбю json передаем строку с ключом {is_taken:False or True}

#Система лайков_________________________________________________________________________

class VotesView(View):
	model = None # Модель данных - Статьи или Комментарии
	vote_type = None # Тип комментария Like/Dislike

	def post(self, request, title):
		obj = self.model.objects.get(title__iexact = title)

		# GenericForeignKey не поддерживает метод get_or_create
		try:
			#Ну и конечно, если вы не захотите добавить обратную связь, вы можете получить доступ к объекту и “обходным путем”:
			likedislike = LikeDislike.objects.get(
				content_type = ContentType.objects.get_for_model(obj),
				object_id = obj.id,
				user = request.user
			)
			if likedislike.vote is not self.vote_type:
				likedislike.vote = self.vote_type
				likedislike.save(update_fields=['vote'])
				result = True
			else:
				likedislike.delete()
				result = False
		except LikeDislike.DoesNotExist:
			obj.votes.create(user = request.user, vote=self.vote_type)#здесь отсылка на generic reletions
			result = True


		print(result)	
		print(obj.votes.likes().count())
		print(obj.votes.dislikes().count())
		print(obj.votes.sum_rating())

		data = {
			'result' : result,
			'like_count' : obj.votes.likes().count(), #эти методы из Menegera модели LikeDislike
			'dislike_count' : obj.votes.dislikes().count(),
			'sum_rating' : obj.votes.sum_rating()
		}
		return JsonResponse(data)
