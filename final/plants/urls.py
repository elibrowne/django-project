from django.urls import path

from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
	path('plant/<str:plantname>/', views.plant.as_view(), name='plantinfo'),
	path('user/<str:username>/', views.user.as_view(), name='userinfo'),
	path('post/<str:post_id>/', views.post.as_view(), name='postcontent'),
	path('newAccount', views.register.as_view(), name='newAcct')
]