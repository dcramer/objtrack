"""
A generic object view tracking model.

This will store a "last viewed date" which says "everything that has changed"
since this date, is unread. It also stores a list of primary keys, which has been
read since that date. These are stored in a text field and separated by
`OBJECT_TRACKING_KEY_SEPARATOR`.

Example use:

from django_object_view_tracking import ObjectTracker

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

def view_thread_list(request):
    threads = Thread.objects.all()
    
    tracking = ObjectTracker.objects.get_for_request(request, Thread)
    
    # This isn't the *best* approach to checking if it's been viewed, but it works
    for thread in threads:
        thread.has_viewed = tracking.has_viewed(thread)
        
    return render(...)

def view_thread(request, thread_id):
    thread = Thread.objects.get(pk=thread_id)

    tracking = ObjectTracker.objects.get_for_request(request, Thread)

    tracking.mark_as_viewed(thread)

    return render(...)
"""

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from django_object_view_tracking.constants import *
from django_object_view_tracking.manager import *

class ObjectTracker(models.Model, ObjectTrackerHandler):
    user            = models.ForeignKey(User)
    content_type    = models.ForeignKey(ContentType)
    date            = models.DateTimeField(blank=True, null=True)
    _objects        = models.TextField(db_column='objects')

    objects         = ObjectTrackerManager()

    def _get_objects(self):
        return self._objects.split(OBJECT_TRACKING_KEY_SEPARATOR)
    
    def _set_objects(self, values):
        self._objects = OBJECT_TRACKING_KEY_SEPARATOR.join(values)
    
    instances = property(_get_objects, _set_objects)