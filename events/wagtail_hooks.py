from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import modeladmin_register

from .views import EventBookingAdmin, event_email_view


modeladmin_register(EventBookingAdmin)

@hooks.register('register_admin_urls')
def register_event_email_url():
    return [
        path('event-email/', event_email_view, name='event-email'),
    ]

@hooks.register('register_admin_menu_item')
def register_calendar_menu_item():
    return MenuItem('Event Email', reverse('event-email'), icon_name='mail', order=300)
