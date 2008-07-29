from django.contrib.contenttypes.models import ContentType

from django_object_view_tracking.constants import *

class ObjectTrackerHandler(object):
    def mark_as_viewed(self, instance, commit=True):
        objects = self.objects
        if instance.pk not in objects:
            objects.append(unicode(instance.pk))
            self.objects = objects
            if commit:
                self.save()

    def mark_all_as_viewed(self, commit=True):
        self.date = datetime.datetime.now()
        if commit:
            self.save()

    def has_viewed(self, instance):
        _has_viewed = unicode(self.object.pk) in self.objects.split(OBJECT_TRACKING_KEY_SEPARATOR)
        if not _has_viewed:
            _has_viewed = self.date and getattr(instance, OBJECT_TRACKING_DATE_ATTRIBUTE) < self.date
        return _has_viewed

class ObjectTrackerSession(ObjectTrackerHandler):
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
    
    def _get_session(self):
        return self.session.get(OBJECT_TRACKING_SESSION_KEY, {})
    
    def _get_objects(self):
        return self._get_session().get('objects', '').split(OBJECT_TRACKING_KEY_SEPARATOR)
    
    def _set_objects(self, values):
        self.session.setdefault(OBJECT_TRACKING_SESSION_KEY, {})['objects'] = OBJECT_TRACKING_KEY_SEPARATOR.join(values)
    
    objects = property(_get_objects, _set_objects)
    
    def _get_date(self):
        return self._get_session().get('date', None)

    def _set_date(self, value):
        self.session.setdefault(OBJECT_TRACKING_SESSION_KEY, {})['date'] = value
        
    date = property(_get_date, _set_date)
    
    def save(self):
        # Handled automatically by Django's sessions
        pass
        
class ObjectTrackerManager(models.Manager):
    def get_for_request(self, request, model_class):
        ct = ContentType.objects.get_for_model(model_class)
        if request.user.is_authenticated():
            try:
                return self.get(user=request.user, content_type=ct)
            except self.model.DoesNotExist:
                return self.model(user=request.user, content_type=ct)
        else:
            return ObjectTrackerSession(request)