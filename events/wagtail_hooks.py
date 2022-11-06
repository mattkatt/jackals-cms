from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem
from wagtail.contrib.modeladmin.options import modeladmin_register

from .models import EventPage
from .views import EventBookingAdmin


@hooks.register("register_admin_menu_item")
def register_bookings_menu_items():
    events: list[EventPage] = EventPage.objects.all()
    event_list = []

    for event in events:
        event_list = event_list + [MenuItem(event.title, f'/admin/bookings/?event_id={event.id}', icon_name='list-ul')]
    event_menu = Menu(items=event_list)

    return SubmenuMenuItem('Bookings', event_menu, icon_name='date')


modeladmin_register(EventBookingAdmin)
