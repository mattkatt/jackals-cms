from wagtail.contrib.modeladmin.options import ModelAdmin
from .models import AdminData


class AdminDataAdmin(ModelAdmin):
    model = AdminData
    base_url_path = 'admin-resources'
    menu_label = 'Admin Resources'
    menu_icon = 'list-ul'
    menu_order = 700
    add_to_settings_menu = True
    exclude_from_explorer = False
    add_to_admin_menu = False
    list_display = (
        'resource_name',
        'resource_url',
        'username',
        'password',
    )
