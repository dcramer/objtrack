from django.db import models
from django.contrib.contenttypes.models import ContentType

import datetime

class ObjectTracker(object):
    """
    tracker = ObjectTracker(request.session)
    tracker.has_viewed(instance, 'date_changed_field_name')
    """
    
    key_name = 'objtracker'
    
    def __init__(self, session):
        self.session = session
    
    def set_date(self, date):
        self.session.setdefault(self.key_name, {})['_date'] = date
    
    def mark_as_viewed(self, instance):
        ct = ContentType.objects.get_for_model(instance.__class__).id
        
        ts = datetime.datetime.now()
        
        if self.key_name not in self.session:
            self.session[self.key_name] = {}
        self.session[self.key_name].setdefault(ct, {})[instance.pk] = ts
        self.session.save()
        
    def mark_all_as_viewed(self, commit=True):
        self.session[self.key_name] = {'_date': datetime.datetime.now()}

    def has_viewed_raw(self, model_class, pk, date_value=None):
        session = self.session.get(self.key_name)
        if not session:
            return False

        # The last date that we say "everything before this has been seen"
        last_date = self.session[self.key_name].get('_date')
        ct = ContentType.objects.get_for_model(model_class).id
        if ct in session:
            last_date = session[ct].get(pk, last_date)
        if not last_date or not date_value:
            return False
        return last_date > date_value

    def has_viewed(self, instance, date_attr=None):
        if date_attr:
            date_value = getattr(instance, date_attr)
        else:
            date_value = None
        return self.has_viewed_raw(instance.__class__, instance.pk, date_value)