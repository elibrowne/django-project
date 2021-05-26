from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views import View

from .models import Plant
from .models import Post
from .models import Profile
from .models import Response
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
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})

		# Check if the user is attempting to view a certain user or plant.
		# The try/catch blocks exist to keep it working when there's no data.
		try: 
			if request.GET['targetusername']:
				return user.as_view()(self.request, request.GET['targetusername'])
		except: 
			print("No target username.")
		
		try: 
			if request.GET['targetplant']:
				return plant.as_view()(self.request, request.GET['targetplant'])
		except: 
			print("No target plant.")

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
		
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})

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
		# Form for login -- available on each page 
		form = AuthenticationForm()
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})
		
		# Create context and go
		context = {
			'plantname': plantname,
			'posts': post_objects.filter(post_plant = Plant.objects.order_by('plant_name').get(plant_name = plantname)),
			'form': form
		}
		return HttpResponse(template.render(context, request))

	def post(self, request, plantname):
		# Post request = the user is making a new post in the plant category
		post_objects = Post.objects.order_by('id')
		template = loader.get_template('plant.html')
		# Form for login -- available on each page 
		form = AuthenticationForm()
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})

		# Add the new post
		if request.POST['postcontent'] != "" and len(request.POST['postcontent']) < 1000 and request.user.is_authenticated:
			newPost = Post(
				post_content = request.POST['postcontent'],
				post_plant = Plant.objects.get(plant_name=plantname),
				post_parent = None, # this is an original post, not a reply
				author = request.user, # person who sent the request is the author
				pub_date = timezone.now(),
				helpful = 0, # both of the "like" values start at zero
				also_questioning = 0,
			)
			newPost.save()
		
		# Load the page, the new post should appear
		context = {
			'plantname': plantname,
			'posts': post_objects.filter(post_plant = Plant.objects.order_by('plant_name').get(plant_name = plantname)),
			'form': form
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
			# Form for login -- available on each page 
			form = AuthenticationForm()
			# Adds placeholders to the fields
			form.fields['username'].widget.attrs.update({
				'placeholder': 'username',
			})
			form.fields['password'].widget.attrs.update({
				'placeholder': 'password'
 			})

			context = {
				'username': username, # not user object because it didn't exist :(
				'form': form
			}
			return HttpResponse(template.render(context, request))
		
		# At this point, we know that the user existed 
		# Get the profile that corresponds to their profile
		profile = Profile.objects.get(user=User.objects.get(username=username))
		template = loader.get_template('user.html')
		context = {
			'posts': Post.objects.filter(author=userInfo.id).order_by('id'),
			'username': userInfo.username,
			'profile': profile
		}
		# Return the template, context, and request, regardless of what they may be
		return HttpResponse(template.render(context, request))

# Post view
class post(View):
	def get(self, request, post_id):
		post_objects = Post.objects.order_by('id')
		template = loader.get_template('post.html')
		form = AuthenticationForm()
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})

		context = {
			'post': get_object_or_404(Post, id=post_id),
			'post_replies': post_objects.filter(post_parent = Post.objects.get(id=post_id)),
			'likes': post_objects.get(id=post_id).likes,
			'helpfuls': post_objects.get(id=post_id).helpful,
			'questions': post_objects.get(id=post_id).also_questioning,
			'celebrations': post_objects.get(id=post_id).celebrating,
			'form': form
		}
		print(request.GET) # testing out the "reply" button that doesn't reply anything
		return HttpResponse(template.render(context, request))

	def post(self, request, post_id):
		postResponse = Response.objects.get_or_create(responseUser=request.user, responsePost=Post.objects.get(id=post_id))[0]
		
		# POST access means that they are sending in a new post that will be a child of this post
		# The user must also be logged in (this is a bonus check, it's already not easy to send a reply when not logged in)
		if request.POST.get('reply', "") != "Input text" and request.POST.get('reply', "") != "" and request.user.is_authenticated:
			newPost = Post(
				post_content = request.POST['reply'],
				# Sorry for the long line here -- Post.objects.get(id=X) was not working :()
				post_plant = Post.objects.get(id=post_id).post_plant, # same as that of parent comment
				post_parent = Post.objects.get(id=post_id),
				author = request.user, # person who sent the request is the author
				pub_date = timezone.now(),
				likes = 0,
				helpful = 0, # both of the "like" values start at zero
				also_questioning = 0,
				celebrating = 0
			)
			newPost.save()
		
		elif request.POST.get('like', "") == "like" and request.user.is_authenticated:
			postResponse.liked = not postResponse.liked # switch the status of the post
			postResponse.save()
			# Increment the counter if the user just liked the post
			if postResponse.liked:
				postToLike = Post.objects.get(id=post_id)
				postToLike.likes += 1
				postToLike.save()
			# Decrement the counter if the user just unliked the post
			else:
				postToLike = Post.objects.get(id=post_id)
				postToLike.likes -= 1
				postToLike.save()

		elif request.POST.get('helped', "") == "helped" and request.user.is_authenticated:
			postResponse.helpful = not postResponse.helpful # switch the status of the post
			postResponse.save()
			# Increment the counter if the user just marked the post as "helpful"
			if postResponse.helpful:
				postToHelp = Post.objects.get(id=post_id)
				postToHelp.helpful += 1
				postToHelp.save()
			# Decrement the counter if the user just unmarked the post as "helpful"
			else:
				postToHelp = Post.objects.get(id=post_id)
				postToHelp.helpful -= 1
				postToHelp.save()

		elif request.POST.get('questioned', "") == "questioned" and request.user.is_authenticated:
			postResponse.questioned = not postResponse.questioned # switch the status of the post
			postResponse.save()
			# Increment the counter if the user just questioned the post
			if postResponse.questioned:
				postToQuestion = Post.objects.get(id=post_id)
				postToQuestion.also_questioning += 1
				postToQuestion.save()
			# Decrement the counter if the user just unliked the post
			else:
				postToQuestion = Post.objects.get(id=post_id)
				postToQuestion.also_questioning -= 1
				postToQuestion.save()

		elif request.POST.get('celebrated', "") == "celebrated" and request.user.is_authenticated:
			postResponse.celebrated = not postResponse.celebrated # switch the status of the post
			postResponse.save()
			# Increment the counter if the user just questioned the post
			if postResponse.celebrated:
				postToQuestion = Post.objects.get(id=post_id)
				postToQuestion.celebrating += 1
				postToQuestion.save()
			# Decrement the counter if the user just unliked the post
			else:
				postToQuestion = Post.objects.get(id=post_id)
				postToQuestion.celebrating -= 1
				postToQuestion.save()

		# New context -- same as old one
		post_objects = Post.objects.order_by('id')
		form = AuthenticationForm()
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})
		
		context = {
			'post': Post.objects.get(id=post_id),
			'post_replies': post_objects.filter(post_parent = Post.objects.get(id=post_id)),
			'likes': post_objects.get(id=post_id).likes,
			'helpfuls': post_objects.get(id=post_id).helpful,
			'questions': post_objects.get(id=post_id).also_questioning,
			'celebrations': post_objects.get(id=post_id).celebrating,
			'form': form
		}
		
		return HttpResponse(loader.get_template('post.html').render(context, request))
