from datetime import date

from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator
from django.db import models
from django.db.models import Model
from django.forms import ModelForm, Textarea
from wagtail.core.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable, Page

from main.helper_methods import append_sidebar_to_context


class EventsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['events.EventPage', ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        events = self.get_children().live()
        context['events'] = events

        append_sidebar_to_context(context)

        return context


class EventBooking(Orderable):
    # region CONSTS
    PLAYER = 'PL'
    MONSTER = 'MN'
    STAFF = 'ST'

    PLAYER_TYPES = [
        (PLAYER, 'Player'),
        (MONSTER, 'Monster'),
        (STAFF, 'Staff')
    ]

    BEARS = 'B'
    DRAGONS = 'D'
    GRYPHONS = 'G'
    HARTS = 'H'
    JACKALS = 'J'
    LIONS = 'L'
    TARANTULAS = 'T'
    UNICORNS = 'U'
    VIPERS = 'V'
    WOLVES = 'W'

    FACTIONS = [
        (BEARS, 'Bears'),
        (DRAGONS, 'Dragons'),
        (GRYPHONS, 'Gryphons'),
        (HARTS, 'Harts'),
        (JACKALS, 'Jackals'),
        (LIONS, 'Lions'),
        (TARANTULAS, 'Tarantulas'),
        (UNICORNS, 'Unicorns'),
        (VIPERS, 'Vipers'),
        (WOLVES, 'Wolves'),
    ]
    # endregion

    event = models.ForeignKey('EventPage', on_delete=models.PROTECT)

    first_name = models.CharField(
        max_length=255, validators=[RegexValidator('^[\\D]*$', message='First name must contain non-digit characters')]
    )
    last_name = models.CharField(
        max_length=255, validators=[RegexValidator('^[\\D]*$', message='Last name must contain non-digit characters')]
    )
    email = models.EmailField(validators=[EmailValidator()])
    contact_number = models.CharField(
        max_length=15, validators=[RegexValidator('^\\+?[\\d-]*$', message='Must be valid phone number format')]
    )

    lt_player_id = models.CharField(
        max_length=15, blank=True, null=True,
        help_text='Required if you have an existing Lorien Trust character (otherwise no blue gold for you!)',
        validators=[RegexValidator('[\\d]', message='Must be valid Lorien Trust Player ID')]
    )
    player_type = models.CharField(max_length=2, choices=PLAYER_TYPES, default=PLAYER)

    character_name = models.CharField(max_length=255, blank=True, null=True)
    character_faction = models.CharField(max_length=1, choices=FACTIONS, verbose_name='Faction', blank=True, null=True)

    is_catering = models.BooleanField(verbose_name='YES, I want food!', default=False)
    has_paid = models.BooleanField(default=False)
    emergency_contact_name = models.CharField(
        max_length=255, validators=[RegexValidator('^[\\D]*$', message='Must contain only non-digit characters')]
    )
    emergency_contact_number = models.CharField(
        max_length=15, validators=[RegexValidator('^\\+?[\\d-]*$', message='Must be valid phone number format')]
    )
    home_address = models.TextField(blank=True)
    medical_information = models.TextField(blank=True)

    panels = [
        FieldPanel('event'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('contact_number'),
        FieldPanel('lt_player_id'),
        FieldPanel('player_type'),
        FieldPanel('character_name'),
        FieldPanel('character_faction'),
        FieldPanel('is_catering'),
        FieldPanel('has_paid'),
        FieldPanel('emergency_contact_name'),
        FieldPanel('emergency_contact_number'),
        FieldPanel('home_address'),
        FieldPanel('medical_information'),
    ]

    def __str__(self):
        booking_str = f"{self.first_name} {self.last_name}"

        if self.character_name:
            booking_str += f" ({self.character_name} - {self.get_character_faction_display()})"

        booking_str += f" [{self.get_player_type_display()}]"
        return booking_str


class EventBookingForm(ModelForm):
    error_class = 'is-danger'

    class Meta:
        model = EventBooking
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'player_type',
            'lt_player_id',
            'player_type',
            'character_name',
            'character_faction',
            'is_catering',
            'emergency_contact_name',
            'emergency_contact_number',
            'home_address',
            'medical_information',
            'has_paid',
        ]
        widgets = {
            'home_address': Textarea(attrs={'rows': 3}),
            'medical_information': Textarea(attrs={'rows': 3}),
        }


class EventPage(Page):
    event_date = models.DateField(verbose_name="Event date")
    intro = models.CharField(max_length=250, default='')
    description = RichTextField(blank=True)
    details = RichTextField(blank=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    player_limit = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    monster_limit = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    player_cost = models.DecimalField(
        verbose_name='Player cost', default=0, max_digits=4, decimal_places=2, validators=[MinValueValidator(0)]
    )
    monster_cost = models.DecimalField(
        verbose_name='Monster cost', default=0, max_digits=4, decimal_places=2, validators=[MinValueValidator(0)]
    )
    player_catering_cost = models.DecimalField(
        verbose_name='Player catering cost', default=0, max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    monster_catering_cost = models.DecimalField(
        verbose_name='Monster catering cost', default=0, max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    catering_name = models.CharField(max_length=250)
    catering_contact_email = models.EmailField()

    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('event_date'),
        FieldPanel('intro'),
        FieldPanel('description'),
        FieldPanel('details'),
        FieldPanel('image'),
        FieldPanel('player_limit'),
        FieldPanel('monster_limit'),
        FieldPanel('player_cost'),
        FieldPanel('monster_cost'),
        FieldPanel('player_catering_cost'),
        FieldPanel('monster_catering_cost'),
        FieldPanel('catering_name'),
        FieldPanel('catering_contact_email'),
    ]

    @property
    def all_bookings(self):
        return EventBooking.objects.filter(event=self)

    @property
    def player_bookings(self):
        return EventBooking.objects.filter(event=self, player_type=EventBooking.PLAYER)

    @property
    def monster_bookings(self):
        return EventBooking.objects.filter(event=self, player_type=EventBooking.MONSTER)

    @property
    def staff_bookings(self):
        return EventBooking.objects.filter(event=self, player_type=EventBooking.STAFF)

    @property
    def has_max_players(self):
        return len(self.player_bookings) >= self.player_limit

    @property
    def has_max_monsters(self):
        return len(self.monster_bookings) >= self.monster_limit

    @property
    def is_concluded(self):
        return date.today() >= self.event_date

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        booking_form = EventBookingForm()
        context['booking_form'] = booking_form
        context['player_bookings'] = self.player_bookings
        context['monster_bookings'] = self.monster_bookings
        context['paypal_client_id'] = settings.PAYPAL_CLIENT_ID
        context['has_max_players'] = self.has_max_players
        context['has_max_monsters'] = self.has_max_monsters
        context['is_concluded'] = self.is_concluded

        append_sidebar_to_context(context)

        return context


class EventEmail(models.Model):
    event = models.ForeignKey('EventPage', on_delete=models.PROTECT)
    player_types = models.CharField(max_length=8, choices=EventBooking.PLAYER_TYPES + [('A', 'All')])
    email_content = models.TextField()
