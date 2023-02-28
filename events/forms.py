from django.forms.widgets import Select
from wagtail.admin.forms import WagtailAdminModelForm

from events.models import EventEmail


class EventEmailForm(WagtailAdminModelForm):
    class Meta:
        model = EventEmail
        fields = ['event','player_types', 'email_content']
        widgets = {
            'event': Select()
        }
