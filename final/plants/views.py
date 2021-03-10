from django.shortcuts import render
from django.http import HttpResponse

# Index view
def index(request):
	return HttpResponse("Index was accessed!")

# Plant view
def plant(request, plantname):
	return HttpResponse("You're looking at " + plantname + "'s plant page.")

# User view
def user(request, username):
	return HttpResponse("You're looking at " + username + "'s user page.")

