from django.urls import path
from .views import *

urlpatterns = [
	#path('', Base),
    path('', FirstList, name = 'first_list_url'),
    path('heading/create/', HeadingCreate.as_view(), name = 'heading_create_url'),
   	path('heading/<str:title>/', ViewHeadingDetail.as_view(), name = 'heading_detail_url'),
    path('blog/', Post, name = 'blog_url'),
    path('blog/<str:title>/', ViewBlogDetail.as_view(), name = 'view_blog_detail_url'),
#   	path('blog/addLike/<int:article_id>/', addLike, name = 'add_like_url'),
    path('learnmore/', LearnMore, name = 'learn_more_url'),
    path('sendmess/', SendContact.as_view(), name = 'send_contact_url'),

]
