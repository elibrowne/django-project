from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('plant/<str:plantname>/', views.plant, name='plantinfo'),
	path('user/<str:username>/', views.user, name='userinfo'),
	path('post/<str:post_id>/', views.post, name='postcontent') # why not int?
]