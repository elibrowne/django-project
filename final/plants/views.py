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
	post_objects = Post.objects.order_by('id')
	template = loader.get_template('plant.html')
	context = {
		'plantname': plantname,
		'posts': post_objects.filter(post_plant = Plant.objects.order_by('plant_name').get(plant_name = plantname[0].upper() + plantname[1:]))
	}
	return HttpResponse(template.render(context, request))

# User view
def user(request, username):
	return HttpResponse("You're looking at " + username + "'s user page.")

# Post view
def post(request, post_id):
	post_objects = Post.objects.order_by('id')
	template = loader.get_template('post.html')
	context = {
		'post': post_objects[int(post_id)],
		'post_replies': post_objects.filter(post_parent = post_objects[int(post_id)])
	}
	return HttpResponse(template.render(context, request))