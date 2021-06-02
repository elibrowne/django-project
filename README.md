# django-project
This is my final Django project for the school year. I think that the most recent commit will be the ideal one to have graded. 

### How to use
This website is divided into "plants" (represented by the 'plant' model), and users can click on those plants from the homepage in order to see the posts specifically related to each plant. On the plant page, users can also create new posts under that category. To interact with a post, the user can click on the post content, which will take them to the 'post' page. The 'post' page displays the post content, the parent post (if it existed), and the replies to the post. If they're logged in, it will then give them the option to "like", "celebrate", "question", or "acknowledge" a post (using the 'response' model). They will also have the ability to respond to the post, creating another 'post' model with the parent_post attribute set to the post they're replying to, or to click on already posted replies. On the home page, it's also possible for the user to go to a 'user' model's page by either entering a username or clicking on a post's author. On this page, users can see any users bio and status (found in the 'profile' model), along with the posts that this user has authored. If the user is viewing their own profile, they'll see the option to edit the bio and status. On the home page, there is lastly an option to register a new user, which is only available when the user is logged out. There is a navigation bar on the top of the screen on every page, which allows for people to log in, log out, and go home. The styling across pages should be consistent. 

### Models
This project uses four models: the plant model, the post model, the profile model, and the response model. It also includes the built in user model.

### User functionality
Users can submit posts to the database and can react to posts with four different reactions (response model in database). Users can log in/out using their username and password. The ability to respond to a post or to make an original post can only be seen when the user is logged in; when the user is logged out, there is simply a prompt for them to log in. As a trend, logged in users have many more options than logged out users on the website (ability to interact, create posts, etc.), but all users should be able to access every page.

### Templates and views
This website has a homepage, pages for each plant, pages for each user, and pages for each post, along with a user not found page. The templates all start similarly (all use the same navbar on the top) and have similar elements (for example, the listing of posts); each serves a different purpose. Lastly, there's a page to register a new user that can bea ccessed from the homepage, which looks different depending on if a user is logged in or logged out. 

### Styling
The website was created using Bootstrap as a starting point. For example, the navigation bars and the buttons are just the basic bootstrap ones with very little changed. Elements were changed for a consistent font (Karla) and color scheme (green). The plant model has an additional plant emoji field to help with those little decorations on the site. 

### Bonus categories
I have worked on the ability to register a user (works), the ability to react to posts and/or comment below them (not super advanced but posts are linked together), and I worked on making the design more advanced (consistent styling across pages, styling of forms including login and registration, fonts, decorations, etc.) (these are the ones we talked about in class).

### Testing invalid inputs and errors
Some of my friends have used the website at different stages of its development for fun, which explains the other posts (not mine haha). I do not know of any bugs or errors (besides 404s when invalid URLs are entered). The character limit on posts seems to be enforced by Django; invalid inputs for logins or registration are dealt with by Django as well. When users input invalid user addresses on the home page, it tells them that the user doesn't exist (in case they're looking for one); in the case of plants, it just refreshes (because plants can be browsed too). When non-logged in users attempt to react to a message, an error message will appear telling them the issue and no reaction will occur. The one thing that I have not styled specifically is the error message for logging in with an invalid password. I have only looked at the emoji rendering on Macs (Safari and Chrome), so I don't know how they would look/if any characters would be nonexistent on other platforms.

#### Checkup One, Step One (April 15)
*project/urls.py* Both a link to an admin site and a forward to plants/urls.py <br />
*app/urls.py* Four entries (including index) to three templates, one filler view (no sample user template yet) <br />
*views.py* Four views, three templates <br />
*templates/plants/.html* Three are currently full HTML files (although they definitely aren't done!). I've experimented with getting data and putting it onto the templates.

#### Checkup One, Step Two (April 15)
*views.py* Views have imported plant and post models, can retrieve data, and can send the data to templates in context.
*templates/plants/.html* Templates (index, plant, post) dump linked posts on the screen. User's page shows associated posts; plant's page shows associated posts; post's page shows post replies (more to come later!). These items link to each other (ie clicking on a post = seeing the entire post).
*models.py* Two models (Plant, Post) and the built-in User model (needs to add login). Each model should have fake data (Plant has a few fake plants and there are a few posts + users admin, eli, and eli2). Plant models have linked posts. Post models have 'parent' plants, authors, and (sometimes) replies in the form of other posts. Users have posts that they've authored.

As of now, the only glitch in the current programmed website that isn't due to not having started is the cherry tomato page being a bit broken, but the three other plant pages give an idea as to what it should look like and how it should function. Fix spaces in URLs soon.
