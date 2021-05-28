# django-project
This is my final Django project for the school year.

### Models
This project uses four models: the plant model, the post model, the profile model, and the response model. It also includes the built in user model.

### User functionality
Users can submit posts to the database and can react to posts with four different reactions. Users can log in/out using their username and password. The ability to respond to a post can only be seen when the user is logged in; when the user is logged out, there is simply a prompt for them to log in.

### Templates and views
This website has a homepage, pages for each plant, pages for each user, and pages for each post, along with a user not found page. The templates all start similarly (all use the same navbar on the top) and have similar elements (for example, the listing of posts); each serves a different purpose.

### Styling
The website was created using Bootstrap as a starting point. For example, the navigation bars and the buttons are just the basic bootstrap ones with very little changed. Elements were changed for a consistent font (Karla) and color scheme (green).

### Bonus categories
I have the ability to register a user, the ability to react to posts and/or comment below them, and I worked on making the design more advanced.

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
