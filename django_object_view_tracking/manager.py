from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_object_view_tracking.constants import *

class ObjectTrackerHandler(object):
    def mark_as_viewed(self, instance, commit=True):
        objects = self.instances
        if instance.pk not in objects:
            objects.append(unicode(instance.pk))
            self.instances = objects
            if commit:
                self.save()

    def mark_all_as_viewed(self, commit=True):
        self.date = datetime.datetime.now()
        if commit:
            self.save()

    def has_viewed_raw(self, pk, date_value):
        _has_viewed = pk in self.instances
        if not _has_viewed:
            _has_viewed = self.date and date_value < self.date
        return _has_viewed or False

    def has_viewed(self, instance):
        return self.has_viewed_raw(instance.pk, getattr(instance, self.date_attr))

class ObjectTrackerSession(ObjectTrackerHandler):
    def __init__(self, request, content_type, date_attr):
        self.session = request.session
        self.user = request.user
        self.content_type = content_type
        self.date_attr = date_attr
    
    def _get_session(self):
        return self.session.get(OBJECT_TRACKING_SESSION_KEY, {}).get(self.content_type.id, {})
    
    def _set_session_value(self, key, value):
        self.session.setdefault(OBJECT_TRACKING_SESSION_KEY, {}).setdefault(self.content_type.id, {})[key] = value
        
    def _get_objects(self):
        return self._get_session().get('objects', '').split(OBJECT_TRACKING_KEY_SEPARATOR)
    
    def _set_objects(self, values):
        self._set_session_value('objects', OBJECT_TRACKING_KEY_SEPARATOR.join(values))
    
    instances = property(_get_objects, _set_objects)
    
    def _get_date(self):
        return self._get_session().get('date', None)

    def _set_date(self, value):
        self._set_session_value('date', value)
        
    date = property(_get_date, _set_date)
    
    def save(self):
        # Handled automatically by Django's sessions
        pass
        
class ObjectTrackerManager(models.Manager):
    def get_for_request(self, request, model_class, date_attr=OBJECT_TRACKING_DATE_ATTRIBUTE):
        ct = ContentType.objects.get_for_model(model_class)
        if request.user.is_authenticated():
            try:
                instance = self.get(user=request.user, content_type=ct)
            except self.model.DoesNotExist:
                instance = self.model(user=request.user, content_type=ct)
            instance.date_attr = date_attr
            return instance
        else:
            return ObjectTrackerSession(request, ct, date_attr)