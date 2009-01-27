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
