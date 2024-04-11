from django.urls import reverse
from wagtail_modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from wagtail.admin.menu import MenuItem

from .models import ProjectType, Genre
from tvweek.models import ChartLine


class GenreAdmin(ModelAdmin):
    model = Genre
    menu_label = 'Жанр'
    menu_icon = 'pick'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)

modeladmin_register(GenreAdmin)


class ProjectTypeAdmin(ModelAdmin):
    model = ProjectType
    menu_label = 'Типи проєктів'
    menu_icon = 'pick'
    menu_order = 205
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


modeladmin_register(ProjectTypeAdmin)


class ChartLineAdmin(ModelAdmin):
    model = ChartLine
    menu_icon = 'pick'
    menu_label = 'Стрічка ТВ програми'
    menu_order = 210
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("start_time", "program_title")
    list_filter = ("program_title", "program_genre")
    search_fields = ("program_title", "program_genre")


modeladmin_register(ChartLineAdmin)


