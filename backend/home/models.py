import os
import logging
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.models import Page, Orderable
from wagtail.admin.panels import InlinePanel, PageChooserPanel, FieldPanel
from wagtail.fields import RichTextField

import tvweek.models
from core.settings import base as core_base

logger = logging.getLogger('lighttv')


class SocialMediaLink(Orderable):
    site_setting = ParentalKey('SocialMediaSettings', related_name='social_media_links')
    name = models.CharField(max_length=255, help_text='Назва соціальної мережі')
    logotype = models.FileField(max_length=255, help_text='Завантажте логотип соціальної мережі')
    url = models.URLField(help_text='URL посилання на соціальну мережу')

    panels = [
        FieldPanel('name'),
        FieldPanel('logotype'),
        FieldPanel('url'),
    ]

    def get_svg_code(self):
        if not self.logotype:
            return ""

        svg_path = os.path.join(core_base.MEDIA_ROOT, self.logotype.name)
        try:
            with open(svg_path, 'r') as file:
                return file.read()
        except IOError:
            return ""


@register_setting
class SocialMediaSettings(BaseSiteSetting, ClusterableModel):
    panels = [
        InlinePanel('social_media_links', label="Соціальні мережі"),
    ]


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
        help_text=_('Малюнок дло блоку Про нас')
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
        now = datetime.now()
        chart_lines_today = tvweek.models.ChartLine.objects.filter(
            start_time__date=now.date(),
            start_time__gt=now
        ).select_related('project_of_program').order_by('start_time')

        context['chart_lines'] = [
            {
                'time': line.start_time.strftime('%H:%M'),
                'program_title': line.program_title,
                'project_title': line.project_of_program.title if line.project_of_program else None
            }
            for line in chart_lines_today
        ]

        return context