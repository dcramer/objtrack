A generic object view tracking model.

This will store a "last viewed date" which says "everything that has changed" since this date, is unread. It also stores a list of primary keys, which has been read since that date.

Install
-------

Download and install the package using distutils::


	pip install objtrack

Update your settings.py and add the installed apps settings::

	INSTALLED_APPS = (
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'objtrack',
	)

Finally, run `python manage.py syncdb` to create the database tables.

Usage
-----

Showing forums which have new posts in them::

	from objtrack.models import ObjectTracker
	
	def view_forum_list(request):
	    categories = Category.objects.all()
    
	    tracking = ObjectTracker.objects.get_for_request(request, Thread)
    
	    # Don't forget you still need to update a date field when a new thread
	    # is added to the forum.
	    for category in categories:
	        category.has_new_posts = tracking.has_viewed(category)

	    # Maybe we want to mark all forums as "i saw this" now?
	    tracking.mark_all_as_viewed()
	    
	    return render(...)


Adding a `has_viewed` attribute to threads in the thread listing::

	def view_thread_list(request):
	    threads = Thread.objects.all()
	    
	    tracking = ObjectTracker.objects.get_for_request(request, Thread)
	    
	    # This isn't the *best* approach to checking if it's been viewed, but it works
	    for thread in threads:
	        thread.has_viewed = tracking.has_viewed(thread)
	    
	    return render(...)


Marking the thread object as read when it's viewed::

	def view_thread(request, thread_id):
	    thread = Thread.objects.get(pk=thread_id)
	    
	    tracking = ObjectTracker.objects.get_for_request(request, Thread)
	    tracking.mark_as_viewed(thread)
	    
	    return render(...)

You can also use it within Coffin or Django templates::

	{% load tracking %}
	
	{% for instance, has_viewed in queryset|with_tracking:"date_field" %}
		...
	{% endfor %}