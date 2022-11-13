from wagtail.contrib.modeladmin.options import modeladmin_register

from .views import EventBookingAdmin


modeladmin_register(EventBookingAdmin)
