from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
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
            if event:
                booking.event = event
                booking.save()
                return HttpResponseRedirect(request.path)
        else:
            raise ValidationError(form.errors)
    except EventPage.DoesNotExist:
        raise ValidationError('No such event')
    except Exception as e:
        raise e

    return HttpResponse(content_type='json')


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
