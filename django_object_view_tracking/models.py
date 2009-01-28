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
    
    def mark_as_viewed(self, instance, commit=True):
        ct = ContentType.objects.get_for_model(instance.__class__).id
        
        ts = datetime.datetime.now()
        
        self.session.setdefault(self.key_name, {}).setdefault(ct, {})[instance.pk] = ts

    def mark_all_as_viewed(self, commit=True):
        self.session[self.key_name] = {'_date': datetime.datetime.now()}

    def has_viewed_raw(self, model_class, pk, date_value=None):
        session = self.session.get(self.key_name)
        if not session:
            return False
            
        last_date = self.session[self.key_name].get('_date')
        if not last_date:
            return False
        
        ct = ContentType.objects.get_for_model(model_class).id
        if ct not in session:
            if date_value < last_date:
                return True
            return False
        
        if not date_value:
            return False
        
        date = session[ct].get(pk, last_date)
        return date_value < date

    def has_viewed(self, instance, date_attr=None):
        if date_attr:
            date_value = getattr(instance, date_attr)
        else:
            date_value = None
        return self.has_viewed_raw(instance.__class__, instance.pk, date_value)