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
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

# Index view - no need to separate GET and POST because there's no practical difference,
# index is only the target of a GET request
class index(View):
	# Get request means that either the user is logged in and wants to stay logged in
	# or that the user is a guest and has not tried to log in. 
	# This view also uses a get request for the two front page forms (quick access) because
	# there is no need to secure that data.
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
			print("No target username.") # using these print statements for console + to have code in the except block
		
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
	# Get just displays the posts and the plant ame
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

	# Post means that the user posted in this plant category, so a new post
	# needs to be added. 
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
				likes = 0,
				celebrating = 0
			)
			newPost.save()
		
		# Load the page, the new post should appear on the new page as it's been added
		context = {
			'plantname': plantname,
			'posts': post_objects.filter(post_plant = Plant.objects.order_by('plant_name').get(plant_name = plantname)),
			'form': form
		}
		return HttpResponse(template.render(context, request))

# User view
class user(View):
	# Get simply displays the user's profile. If the user is logged in and is viewing
	# their own profile, there will be an option to edit that profile, but that is dealt
	# with in the template using if user.is_authenticated.
	def get(self, request, username):
		template = loader.get_template('user.html')
		# Create authentication form
		form = AuthenticationForm()
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})

		# Check if the user exists
		try:
			userInfo = User.objects.filter(username=username)[0]
		except:
			# Load the user not found template
			template = loader.get_template('nouser.html')
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
			'profile': profile,
			'form': form
		}
		# Return the template, context, and request, regardless of what they may be
		return HttpResponse(template.render(context, request))
	
	# The post method is only used when the user edited their own profile data.
	# It is very similar to the get template, the sole difference being saving data.
	def post(self, request, username):	
		template = loader.get_template('user.html')
		# Create authentication form
		form = AuthenticationForm()
		# Adds placeholders to the fields, per usual
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})

		# Check if the user exists: keeping this although it probably won't be an issue
		# Still need to get the user object anyways
		try:
			userInfo = User.objects.filter(username=username)[0]
		except:
			# Load the user not found template
			template = loader.get_template('nouser.html')
			context = {
				'username': username, # not user object because it didn't exist :(
				'form': form
			}
			return HttpResponse(template.render(context, request))
		
		# At this point, we know that the user existed 
		# Get the profile that corresponds to their profile
		profile = Profile.objects.get(user=User.objects.get(username=username))
		# Update their profile with the specified changes
		profile.bio = request.POST.get('bio', "") # empty field results in empty
		profile.status = request.POST.get('status', "")
		profile.save()

		# load the website
		template = loader.get_template('user.html')
		context = {
			'posts': Post.objects.filter(author=userInfo.id).order_by('id'),
			'username': userInfo.username,
			'profile': profile,
			'form': form
		}
		# Return the template, context, and request, regardless of what they may be
		return HttpResponse(template.render(context, request))

# Post view
class post(View):
	# The get method just displays the post and the options to interact with it.
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

	# The post method here has to deal with a variety of things. If the user 
	# replies to a post, it must add the response and save it. If the user reacts,
	# it must accurately update both the Post and Response models. 
	def post(self, request, post_id):
		# Variable to check if an error message is needed (non logged in user tried to interact)
		needsWarning = False
		# This is only here because there is never an error messaged needed with a GET request
		
		if request.user.is_authenticated:
			# The user can only interact with the post significantly if they're logged in.
			postResponse = Response.objects.get_or_create(responseUser=request.user, responsePost=Post.objects.get(id=post_id))[0] 

			# Replying to the post:
			if request.POST.get('reply', "") != "Input text" and request.POST.get('reply', "") != "":
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
			
			# Reacting to the post (four different reactions):

			elif request.POST.get('like', "") == "like":
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

			elif request.POST.get('helped', "") == "helped":
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

			elif request.POST.get('questioned', "") == "questioned":
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

			elif request.POST.get('celebrated', "") == "celebrated":
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
		else:
			# Alert the user that they must be logged in to interact with a post
			needsWarning = True 

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
			'form': form,
			'needsWarning': needsWarning
		}
		
		return HttpResponse(loader.get_template('post.html').render(context, request))

# Register a new user view
# The register class only displays the options to create a new user when the user
# is not logged in, regardless of whether get or post is used. This is done with
# an if block and user.is_authenticated.
class register(View):
	# Get method displays the options to make a new user
	def get(self, request):
		template = loader.get_template('register.html')
		form = AuthenticationForm()
		newAcctForm = UserCreationForm() # also a django default
		
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})
		# Add placeholders to the new account form fields
		newAcctForm.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		newAcctForm.fields['password1'].widget.attrs.update({
			'placeholder': 'password'
 		})
		newAcctForm.fields['password2'].widget.attrs.update({
			'placeholder': 'confirm password'
 		})

		context = {
			'newAcctForm': newAcctForm,
			'form': form,
			'warnings': ""
		}

		return HttpResponse(template.render(context, request))

	# This method runs after the user attempts to create their account.
	def post(self, request):
		# When there is a post request on the registration page, the website user attempted to make an account
		warnings = "" # will add warnings if there are issues with their registration!
		# User is logging in
		newAcctForm = UserCreationForm(data=request.POST)
		# Validate and clean the data
		if newAcctForm.is_valid():
			newAcctForm.save() # create the new user (?)

			username = newAcctForm.cleaned_data['username']
			password = newAcctForm.cleaned_data['password1']
			
			# Log the user in so they don't see the failed form again
			user = authenticate(username = username, password=password)
			if user is not None:
				login(request, user=user)
			
			# Create the user's profile
			newProfile = Profile(
				user = user,
				bio = "",
				status = ""
			)
			newProfile.save()
		
		else:
			# The form wasn't valid, change the error message and go back to registration page
			# Append each error to the list of errors (warning String)
			for field in newAcctForm:
				for error in field.errors:
					warnings += error + " "
			
			
		template = loader.get_template('register.html') 

		newAcctForm = UserCreationForm()
		form = AuthenticationForm()
		# Adds placeholders to the fields
		form.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		form.fields['password'].widget.attrs.update({
			'placeholder': 'password'
 		})
		# Add placeholders to the new account form fields
		newAcctForm.fields['username'].widget.attrs.update({
			'placeholder': 'username',
		})
		newAcctForm.fields['password1'].widget.attrs.update({
			'placeholder': 'password'
 		})
		newAcctForm.fields['password2'].widget.attrs.update({
			'placeholder': 'confirm password'
 		})
		
		context = {
			'newAcctForm': newAcctForm,
			'form': form,
			'warnings': warnings
		}

		return HttpResponse(template.render(context, request))