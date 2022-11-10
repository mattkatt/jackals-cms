from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.models import Page

from main.helper_methods import append_sidebar_to_context


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

        append_sidebar_to_context(context)

        return context
