# django-project
Django project

### Checkup One, Step One (April 15)
*project/urls.py* Both a link to an admin site and a forward to plants/urls.py <br />
*app/urls.py* Four entries (including index) to three templates, one filler view (no sample user template yet) <br />
*views.py* Four views, three templates <br />
*templates/plants/.html* Three are currently full HTML files (although they definitely aren't done!). I've experimented with getting data and putting it onto the templates.

### Checkup One, Step Two (April 15)
*views.py* Views have imported plant and post models, can retrieve data, and can send the data to templates in context.
*templates/plants/.html* Templates (index, plant, post) dump linked posts on the screen. User's page shows associated posts; plant's page shows associated posts; post's page shows post replies (more to come later!). These items link to each other (ie clicking on a post = seeing the entire post).
*models.py* Two models (Plant, Post) and the built-in User model (needs to add login). Each model should have fake data (Plant has a few fake plants and there are a few posts + users admin, eli, and eli2). Plant models have linked posts. Post models have 'parent' plants, authors, and (sometimes) replies in the form of other posts. Users have posts that they've authored.
