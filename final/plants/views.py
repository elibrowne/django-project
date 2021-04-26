from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View

from .models import Plant
from .models import Post
from .models import Profile
from django.contrib.auth.models import User 

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

# Index view - no need to separate GET and POST because there's no practical difference,
# index is only the target of a GET request
class index(View):
	# Get request means that either the user is logged in and wants to stay logged in
	# or that the user is a guest and has not tried to log in. 
	def get(self, request):
		# Variables
		plant_objects = Plant.objects.order_by('plant_name') # to be passed to the homepage
		template = loader.get_template('index.html')
		form = AuthenticationForm()
		# Context for the template
		context = {
			'form': form,
			'plant_objects': plant_objects,
		}
		return HttpResponse(template.render(context, request))
	
	# Post request means that the user just logged in or logged out.
	def post(self, request): 
		# Variables (again used logged in or out)
		plant_objects = Plant.objects.order_by('plant_name') # to be passed to the homepage
		template = loader.get_template('index.html')

		# If the user logged out, just log them out
		if 'logout' in request.POST.keys():
			logout(request)
			# We load an empty form with no data
			form = AuthenticationForm()
		else:
			# User is logging in
			form = AuthenticationForm(data=request.POST)
			# Validate and clean the data
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				# Then authenticate and log in.
				user = authenticate(username = username, password=password)
				if user is not None:
					login(request, user=user)
		
		# Set up context with form and plant objects
		context = {
			'form': form,
			'plant_objects': plant_objects,
		}
		return HttpResponse(template.render(context, request))

# Plant view (basic)
class plant(View):
	def get(self, request, plantname):
		post_objects = Post.objects.order_by('id')
		template = loader.get_template('plant.html')
		context = {
			'plantname': plantname,
			'posts': post_objects.filter(post_plant = Plant.objects.order_by('plant_name').get(plant_name = plantname[0].upper() + plantname[1:]))
		}
		return HttpResponse(template.render(context, request))

# User view
class user(View):
	def get(self, request, username):
		template = loader.get_template('user.html')
		# Check if the user exists
		try:
			userInfo = User.objects.filter(username=username)[0]
		except:
			template = loader.get_template('nouser.html')
			context = {
				'username': username # not user object because it didn't exist :(
			}
			return HttpResponse(template.render(context, request))
		
		# At this point, we know that the user existed (would've returned nouser.html otherwise)
		template = loader.get_template('user.html')
		context = {
			'posts': Post.objects.filter(author=userInfo.id).order_by('id'),
			'username': userInfo.username,
			# 'status': userInfo.status # TODO STILL NEED TO WORK ON PROFILE!
		}
		# Return the template, context, and request, regardless of what they may be
		return HttpResponse(template.render(context, request))

# Post view
class post(View):
	def get(self, request, post_id):
		post_objects = Post.objects.order_by('id')
		template = loader.get_template('post.html')
		context = {
			'post': post_objects[int(post_id)],
			'post_replies': post_objects.filter(post_parent = post_objects[int(post_id)])
		}
		print(request.GET) # testing out the "reply" button that doesn't reply anything
		return HttpResponse(template.render(context, request))