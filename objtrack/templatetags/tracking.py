from objtrack.models import ObjectTracker

try:
    from coffin import template
except ImportError:
    from django import template

register = template.Library()

@register.filter()
def with_tracking(queryset, session, date_field=None):
    tracker = ObjectTracker(session)
    for obj in queryset:
        yield obj, tracker.has_viewed(obj, date_field)