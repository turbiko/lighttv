from django.urls import reverse
from wagtail_modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from wagtail.admin.menu import MenuItem

from .models import ProjectType

class ProjectTypeAdmin(ModelAdmin):
    model = ProjectType
    menu_label = 'Типи проєктів'
    menu_icon = 'pick'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


modeladmin_register(ProjectTypeAdmin)