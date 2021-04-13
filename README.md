# django-project
Django project

### Checkup One, Step One (April 15)
*project/urls.py* Both a link to an admin site and a forward to plants/urls.py <br />
*app/urls.py* Four entries (including index) to three templates, one filler view (no sample user template yet) <br />
*views.py* Four views, three templates <br />
*templates/plants/.html* Three are currently full HTML files (although they definitely aren't done!). I've experimented with getting data and putting it onto the templates.

### Checkup One, Step Two (April 15)
*views.py* Views have imported (some) models and can send the data to templates in context
*templates/plants/.html* Templates (index, plant, post) dump linked posts on the screen. User template still does not.
*models.py* Two models (Plant, Post) and the built-in User model (needs to add login). Each model should have fake data (Plant has a few fake plants and there are a few posts).