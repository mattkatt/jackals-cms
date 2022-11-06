from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from wagtail.contrib.modeladmin.options import ModelAdmin

from events.models import EventBookingForm, EventPage, EventBooking


# Create your views here.
def submit_event_booking(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Method not allowed')

    form = EventBookingForm(request.POST)

    try:
        if form.is_valid():
            booking: EventBooking = form.instance
            event = EventPage.objects.get(id=request.POST['event_id'])
            booking.event = event
            booking.save()
            messages.success(request, 'Your booking has been successful! We look forward to seeing you at the event.',
                             'is-success')
        else:
            raise ValidationError(form.errors)
    except EventPage.DoesNotExist:
        messages.error(request, 'The event you have tried to book does not exist. If you have paid via paypal, '
                                'please contact the Jackals Faction for a refund.', 'is-danger')
        raise ValidationError('No such event')
    except Exception as e:
        messages.error(request, 'There has been an unresolvable error. If you have paid via paypal, please contact '
                                'the Jackals Faction for a refund.', 'is-danger')
        raise e

    return HttpResponseRedirect(event.url)


class EventBookingAdmin(ModelAdmin):
    model = EventBooking
    base_url_path = 'bookings'
    menu_icon = 'list-ul'
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = False
    list_display = (
        'first_name',
        'last_name',
        'email',
        'contact_number',
        'lt_player_id',
        'player_type',
        'character_name',
        'character_faction',
        'is_catering',
    )
    list_filter = ('event_id', )
    list_export = (
        'first_name',
        'last_name',
        'email',
        'contact_number',
        'lt_player_id',
        'player_type',
        'character_name',
        'character_faction',
        'is_catering',
        'emergency_contact_name',
        'emergency_contact_number',
        'home_address',
        'medical_information',
    )
