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

    data = request.POST
    event = EventPage.objects.get(id=data['event_id'])

    booking = EventBooking()
    booking.event = event

    booking.first_name = data['first_name'].capitalize()
    booking.last_name = data['last_name'].capitalize()
    booking.email = data['email']
    booking.contact_number = data['contact_number']
    booking.lt_player_id = data['lt_player_id'] if data['lt_player_id'] != '' else None
    booking.player_type = data['player_type']
    booking.character_name = data['character_name'].capitalize() if data['character_name'] != '' else None
    booking.character_faction = data['character_faction'] if data['character_faction'] != '' else None
    booking.emergency_contact_name = data['emergency_contact_name'].capitalize()
    booking.emergency_contact_number = data['emergency_contact_number']
    booking.home_address = data['home_address']
    booking.medical_information = data['medical_information']

    booking.is_catering = False
    booking.has_paid = False

    if 'is_catering' in data.values():
        booking.is_catering = True

    if 'has_paid' in data.values():
        booking.has_paid = True

    try:
        booking.save()

        messages.success(
            request,
            f'Your booking has been successful! We look forward to seeing you at the event. Booking name: {booking.first_name} {booking.last_name}, Booking type: {booking.get_player_type_display()}',
            'is-success',
        )
    except Exception as e:
        messages.error(request, 'There has been an unresolvable error. If you have paid via paypal, please contact '
                                'the Jackals Faction for a refund.', 'is-danger')

    return HttpResponseRedirect(event.url)


class EventBookingAdmin(ModelAdmin):
    model = EventBooking
    base_url_path = 'bookings'
    menu_label = 'Event Bookings'
    menu_icon = 'list-ul'
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = (
        'id',
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
    list_filter = ('event', )
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
        'has_paid',
        'emergency_contact_name',
        'emergency_contact_number',
        'home_address',
        'medical_information',
    )
    search_fields = ('id', 'email', 'first_name', 'last_name', 'lt_player_id', )
