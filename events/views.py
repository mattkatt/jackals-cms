from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

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
