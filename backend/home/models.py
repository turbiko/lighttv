import os
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Page, Orderable
from wagtail.admin.panels import InlinePanel, PageChooserPanel

logger = logging.getLogger('lighttv')


@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(
        help_text='Facebook URL', default='#')
    instagram = models.URLField(
        help_text='Instagram URL', default='#')
    tiktok = models.URLField(
        help_text='Tiktok URL', default='#')
    youtube = models.URLField(
        help_text='YouTube URL', default='#')


class HomePageSliderImages(Orderable):
    """big slider images for slider on home page"""
    page = ParentalKey('wagtailcore.Page', related_name='slider_images')
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.CASCADE)

    panels = [
        PageChooserPanel('project', 'project.Project'),
    ]


class HomePage(Page):

    content_panels = Page.content_panels + [
        InlinePanel('slider_images', label="Slider images"),
        # Додайте інші поля тут
    ]

    def get_context(self, request):
        logger.info(f'Homepage (get_context) was accessed by {request.user} ')
        context = super().get_context(request)
        return context