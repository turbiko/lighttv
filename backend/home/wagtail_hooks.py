# from wagtail_modeladmin.options import (
#     ModelAdmin,
#     modeladmin_register,
#     ModelAdminGroup,
# )
#
# from .models import HomePageAboutText
#
#
# class HomePageAboutTextAdmin(ModelAdmin):
#     model = HomePageAboutText
#     menu_label = 'HomePageAboutText'
#     menu_icon = 'pick'
#     menu_order = 200
#     add_to_settings_menu = False
#     exclude_from_explorer = False
#     list_display = ("name",)
#     list_filter = ("name",)
#     search_fields = ("name",)
#
#
# modeladmin_register(HomePageAboutTextAdmin)