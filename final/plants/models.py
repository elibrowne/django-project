from django.db import models
from django.contrib.auth.models import User # for the user

# Plant class -- no major information for now if there aren't any polls (which may be added later)
class Plant(models.Model):
	plant_name = models.CharField(max_length=100) # no limit -- these will not be generated by users
	plant_type = models.CharField(max_length=20, null=True, blank=True) # fruit, vegetable, herb, etc. 
	def __str__(self):
		return self.plant_name


# Posts: have an associated plant and text. 
# Each post has a relationship with one user (author), but users can have multiple posts.
# Each post has a relationsihp with one plant, but plants should have multiple posts.
class Post(models.Model):
	# Content pertaining to each post 
	post_content = models.CharField(max_length=1000) # in case there is a lot of explaining to do :)
	post_plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True, default=None) # when the plant is deleted (shouldn't happen), remove posts

	# User model content (from Dr. Jaiclin)
	author = models.ForeignKey(User, on_delete=models.CASCADE) # had to add null possibility?
	pub_date = models.DateTimeField('date published')

	# Only used if a post is replying to a parent post
	post_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None) # post deletes if the parent post deletes

	# Using two different metrics to measure support for a post rather than likes
	helpful = models.IntegerField(default=0) # for people who think the most is helpful (basically a 'like')
	also_questioning = models.IntegerField(default=0) # a 'like' to indicate that other people have the same issue

	def __str__(self): 
		# This is the string returned when asked to stringify the post
		stringified = "On " + str(self.pub_date) + ", " + str(self.author) + " said...\n\n"
		stringified += self.post_content + "\n\n" # add the actual content as a paragraph in the middle
		stringified += "in the " + self.post_plant.plant_name + " category."
		# Finished string includes all the important information
		return stringified

# Profile is in a one-to-one relationship with Django's user object.
# This is used only for the profile pages. 
# THIS IS STILL IN PROGRESS AND IT DOESNT REALLY WORK RIGHT NOW! ://
class Profile(models.Model):
	user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
	status = models.TextField(default="", blank=True)
	# Stringify the class is just done via the username
	def __str__(self):
		return user.username

