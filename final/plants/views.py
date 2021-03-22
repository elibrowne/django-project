from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Plant
from .models import Post

# Index view
def index(request):
	plant_objects = Plant.objects.order_by('plant_name') # to be passed to the homepage
	template = loader.get_template('index.html')
	context = {
		'plant_objects': plant_objects,
	}
	return HttpResponse(template.render(context, request))

# Plant view (basic)
def plant(request, plantname):
	return HttpResponse("You're looking at " + plantname + "'s plant page.")

# User view
def user(request, username):
	return HttpResponse("You're looking at " + username + "'s user page.")

# Post view
def post(request, post_id):
	post_objects = Post.objects.order_by('id')
	template = loader.get_template('post.html')
	context = {
		'post': post_objects[int(post_id)],
		# POST REPLIES OBJECT <3
	}
	return HttpResponse(template.render(context, request))