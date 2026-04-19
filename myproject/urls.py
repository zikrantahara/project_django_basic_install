from django.contrib import admin
from django.urls import path, include
from . import views 
from myapp import views as myapp_views 
from django.views.generic import TemplateView, ListView
from myapp.models import Dreamreal
from myapp.feeds import DreamrealCommentsFeed

handler404 = views.handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include("products.urls")),
    path('customers/', include("customers.urls")),
    path('myapp/', include("myapp.urls")),
    path('home/', views.index, name='home'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('addnew/', myapp_views.addnew, name='addnew'),
    path('update/<int:pk>/', myapp_views.update_data, name='update'),
    path('delete/<int:pk>/', myapp_views.delete_data, name='delete'),
    path('cities/', myapp_views.show_cities, name='cities'),
    path('hello/', myapp_views.hello, name='hello'),
    path('articles/<str:year>/<str:month>/', myapp_views.viewArticles, name='articles'),
    path('article/<int:articleId>/', myapp_views.viewArticle, name='article'),
    path('simpleemail/<str:emailto>/', myapp_views.sendSimpleEmail, name='sendSimpleEmail'),
    path('adminsemail/', myapp_views.sendAdminsEmail, name='sendAdminsEmail'),
    path('attachemail/<str:emailto>/', myapp_views.sendEmailWithAttach, name='sendEmailWithAttach'),
    path('static-page/', TemplateView.as_view(template_name='static.html'), name='static'),
    path('dreamreals/', ListView.as_view(model=Dreamreal, template_name='dreamreal_list.html'), name='dreamreal_list'),
    path('login/', myapp_views.login, name='login'),
    path('myapp-login/', myapp_views.login, name='myapp_login'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('saved/', myapp_views.SaveProfile, name='saved'),
    path('connection/', myapp_views.formView, name='connection'),
    path('logout/', myapp_views.logout, name='logout'),
    path('test-cache/', myapp_views.view_caching, name='test_cache'),
    path('comments/', include('django_comments.urls')),
    path('hello/<str:Name>/', myapp_views.hello, name='hello'),
    path('latest/comments/', DreamrealCommentsFeed(), name='latest_comments'),
    path('comment/<int:object_pk>/', myapp_views.comment, name='comment'),
    path('dreamreal/', myapp_views.dreamreal_ajax, name='dreamreal'),
]