from django.shortcuts import render

from .models import *
from .forms import *
from django.views.generic import View
from django.shortcuts import get_object_or_404
from translate.utils import *

from django.db.models import Q

from django.shortcuts import redirect
from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from likes.models import Like

from django.views.decorators.http import require_http_methods
import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail
from myfirst import settings
from django.template.context_processors import csrf

from django.shortcuts import render_to_response
from django.utils import timezone

#def Base(request):
#	headings = Heading.objects.all()
#	return render(request, 'translate/first_list.html', context = {'headings': headings})

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
class HeadingCreate(View):
	
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

#	@require_http_methods(["POST"])
#	def add_comment(request, title):
	def post(self, request, *args, **kwargs):
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



