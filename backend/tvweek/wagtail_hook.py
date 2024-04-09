
from wagtail_modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)

from .models import ChartLine, TVChart


class ChartLineAdmin(ModelAdmin):
    model = ChartLine
    menu_icon = 'pick'
    menu_label = 'ChartLine'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("start_time", "program_title", "program_genre")
    list_filter = ("start_time", "program_title", "program_genre")
    search_fields = ("program_title", "program_genre")


modeladmin_register(ChartLineAdmin)