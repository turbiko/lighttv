import os
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Page, Orderable
from wagtail.admin.panels import InlinePanel, PageChooserPanel, FieldPanel
from wagtail.fields import RichTextField

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


class HomeTvManualStep(Orderable):
    page = ParentalKey('wagtailcore.Page', related_name='manual_step')
    about_name = models.CharField(max_length=150, blank=True, null=True)
    step_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('малюнок дло блоку Про нас')
    )


class HomeOnlineTv(Orderable):
    page = ParentalKey('wagtailcore.Page', related_name='online_tv')
    online_provider_url = models.URLField(default="#")
    logo_provider = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Логотип провайдера')
    )


class HomePage(Page):
    about_name = models.CharField(max_length=50, blank=True,null=True)
    about_title = models.CharField(max_length=50, blank=True,null=True)
    about_description = RichTextField( blank=True,null=True)
    about_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('малюнок дло блоку Про нас')
    )
    manual_name = models.CharField(max_length=150, blank=True,null=True)
    manual_title = models.CharField(max_length=250, blank=True,null=True)
    manual_text = models.CharField(max_length=550, blank=True,null=True)
    online_name = models.CharField(max_length=150, blank=True,null=True)
    online_title = models.CharField(max_length=250, blank=True,null=True)
    online_text = RichTextField( blank=True,null=True)


    content_panels = Page.content_panels + [
        FieldPanel('about_name'),
        FieldPanel('about_title'),
        FieldPanel('about_description'),
        FieldPanel('about_picture'),
        InlinePanel('slider_images', label="Малюнки для слайдеру"),
        FieldPanel('manual_name'),
        FieldPanel('manual_title'),
        FieldPanel('manual_text'),
        InlinePanel('manual_step', label="Малюнки до інструкції на головній сторінці"),
        FieldPanel('online_name'),
        FieldPanel('online_title'),
        FieldPanel('online_text'),
        InlinePanel('online_tv', label="Логотип онлайн провайдера"),
    ]

    def get_context(self, request):
        logger.info(f'Homepage (get_context) was accessed by {request.user} ')
        context = super().get_context(request)

        return context