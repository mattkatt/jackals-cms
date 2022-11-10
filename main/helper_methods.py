from django.apps import apps
from wagtail.models import Page


def append_sidebar_to_context(context):
    try:
        events: Page = apps.get_model(app_label='events', model_name='EventPage')
        latest_event = events.objects.filter(live=True).latest('event_date')
    except Page.DoesNotExist:
        latest_event = None

    context['latest_event'] = latest_event

    try:
        library_index = apps.get_model(app_label='library', model_name='LibraryIndexPage')
        library_first_level_children = library_index.objects.first().get_children()
    except Page.DoesNotExist:
        library_first_level_children = None

    context['library_areas'] = library_first_level_children
