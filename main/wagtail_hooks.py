from wagtail.contrib.modeladmin.options import modeladmin_register

from .views import AdminDataAdmin


modeladmin_register(AdminDataAdmin)
