from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required#декоратор огроничения доступа, здксь не используется @, а просто обьект на который есть огроничение захватывается в кавычки
from .decorators import check_recaptcha
from .view import * 
# настройки предназначенные для фильтрации и поиска пользователей
from django_filters.views import FilterView #это специальный класс
from .filters import UserFilter

urlpatterns = [
	#path('', Base),
    path('', FirstList, name = 'first_list_url'),
    path('log/', MyLoginView.as_view(), name = 'log_url'),#эксперементальный
    path('logout/', myLogout, name = 'logout_url'),
    path('heading/create/', HeadingCreate.as_view(), name = 'heading_create_url'),
   	path('heading/<str:title>/', ViewHeadingDetail.as_view(), name = 'heading_detail_url'),
   
    path('blog/', Post.as_view(), name = 'blog_url'),
    path('blog/<str:title>/', ViewBlogDetail.as_view(), name = 'view_blog_detail_url'),
    #система добавление и удоление закладок, здесь могут закладки добовлять тольео зарегистрированные пользователи  
    path('blog/<str:title>/ajax/', login_required(BookmarkView.as_view(modelbookmark = BookmarkBlog)), name = 'blog_bookmark'),
#   	path('blog/addLike/<int:article_id>/', addLike, name = 'add_like_url'),
    path('learnmore/', LearnMore, name = 'learn_more_url'),
    path('sendmess/', SendContact.as_view(), name = 'send_contact_url'),
    
    #регистрация пользователя # reCAPTCHA
    path('signup/', check_recaptcha(SignUpView.as_view()), name='signup'),

    #проверка существующего пользователя с использованием ajax 
    path('ajax/validate_username/', validate_username, name = 'validate_username'),

    # ajax система лайков_______________
    path('blog/<str:title>/like/', login_required(VotesView.as_view(model = Blog, vote_type = LikeDislike.LIKE)), name = 'blog_like_url'),
    path('blog/<str:title>/dislike', login_required(VotesView.as_view(model = Blog, vote_type = LikeDislike.DISLIKE)), name = 'blog_dislike_url'),

    #Смена URL без перезагрузки страницы с частичной подгрузкой контента
    path('ajax/pagination/', indexVi.as_view(), name='index_url'),

    #download data users excel
    path('export/csv/', export_exel.export_users_csv, name='export_users_csv'),
    #Using WeasyPrint преобразовывает html в pdf фомат
#   path('export/pdf/', html_to_pdf_view, name = 'html_to_pdf_view_url'), здесь я не разобрался с установкой данного модуля
    
    #Загрузка мультифайлов(несколько)
    path('progress-bar-upload/', multiple_upload.ProgressBarUploadView.as_view(), name='progress_bar_upload_url'),
    
    #Filter QuerySets
    #path('search/', queryset_filter.search, name = 'search_url'),
    #Filter QuerySets это тоже фильтр но только с использованием  Generic Class-Based View
    # здесь уже готовоя функция, и не надо подключать вьюху, просто есть аргумент где указ filterset_class=UserFilter
    path('search/', FilterView.as_view(filterset_class=UserFilter, template_name='queryset_filter/user_list.html'), name='search_url'),
]


    
 