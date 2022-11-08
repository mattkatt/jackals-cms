from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from wagtail.contrib.modeladmin.options import ModelAdmin

from events.models import EventBookingForm, EventPage, EventBooking


# Create your views here.
def validate_event_form(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Method not allowed')

    form = EventBookingForm(request.POST)
    event_id = request.POST['event_id']

    try:
        event = EventPage.objects.get(id=event_id)
        if event.is_concluded:
            return HttpResponse(
                content=f'{"event_error": "event_id ${event_id} concluded"}',
                content_type='application/json',
                status=401
            )
    except EventPage.DoesNotExist:
        return HttpResponse(
            content=f'{"event_error": "event_id ${event_id} does not exist"}',
            content_type='application/json', status=401
        )

    if not form.is_valid():
        return HttpResponse(content=form.errors.as_json(), content_type='application/json', status=401)

    return HttpResponse(content=True, content_type='application/json')


def submit_event_booking(request):
    if request.method != "POST":
        return HttpResponseBadRequest('Method not allowed')

    form = EventBookingForm(request.POST)

    try:
        booking: EventBooking = form.instance
        event = EventPage.objects.get(id=request.POST['event_id'])
        booking.event = event
        booking.save()
        messages.success(request, 'Your booking has been successful! We look forward to seeing you at the event.',
                         'is-success')
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
