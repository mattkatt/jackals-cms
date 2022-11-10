from django.apps import apps
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]

    subpage_types = [
        'events.EventsIndexPage',
        'library.LibraryIndexPage',
        'library.LibraryCategoryIndexPage',
        'library.LibraryTagIndexPage',
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        try:
            events: Page = apps.get_model(app_label='events', model_name='EventPage')
            latest_event = events.objects.latest('event_date')
        except Page.DoesNotExist:
            latest_event = None

        context['latest_event'] = latest_event

        try:
            library_index = apps.get_model(app_label='library', model_name='LibraryIndexPage')
            library_first_level_children = library_index.objects.first().get_children()
        except Page.DoesNotExist:
            library_first_level_children = None

        context['library_areas'] = library_first_level_children

        return context
