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
from wagtail.documents import get_document_model

import tvweek.models
from core.settings import base as core_base
from tools.owerwritefile import OverwriteStorage


logger = logging.getLogger('lighttv')


class Contact(models.Model):
    name = models.CharField(max_length=230, verbose_name='Ім’я')
    email = models.EmailField(max_length=255, verbose_name='Електронна пошта')
    message = models.TextField(verbose_name='Повідомлення')

    def __str__(self):
        return f"Contact {self.name}"


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


class ReportPDF(Orderable):
    site_setting = ParentalKey('ReportPDFSettings', related_name='report_pdf')
    title = models.CharField(max_length=200)
    report = models.FileField(
        max_length=255,
        help_text='Структура власності',
        storage=OverwriteStorage()
    )

class ContactData(Orderable):
    site_setting = ParentalKey('ContactDataSettings', related_name='contact_data')
    phone = models.CharField(max_length=200, blank=True, null=True)
    post_addr = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)

@register_setting
class SocialMediaSettings(BaseSiteSetting, ClusterableModel):
    panels = [
        InlinePanel('social_media_links', label="Соціальні мережі"),
    ]


@register_setting
class ReportPDFSettings(BaseSiteSetting, ClusterableModel):
    panels = [
        InlinePanel('report_pdf', label="Структура власності"),
    ]

@register_setting
class ContactDataSettings(BaseSiteSetting, ClusterableModel):
    panels = [
        InlinePanel('contact_data', label="Контактні дані", max_num=1),
    ]

    def get_contact_data(self):
        return self.contact_data.first()  # Повертаємо перший запис

    class Meta:
        verbose_name = "Налаштування контактних даних"

class HomePageSliderImages(Orderable):
    """big slider images for slider on home page"""
    page = ParentalKey('wagtailcore.Page', related_name='slider_images')
    project = models.ForeignKey('project.Project', null=True, blank=True, on_delete=models.CASCADE)
    desktop_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Малюнок слайдеру десктоп версія')
    )
    mobile_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Малюнок слайдеру мобільна версія')
    )


    panels = [
        PageChooserPanel('project', 'project.Project'),
        FieldPanel('desktop_picture'),
        FieldPanel('mobile_picture')
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


class HomeOnlineTv(Orderable):  # Online providers section
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
    about_name = models.CharField(_('Про нас назва блоку'), max_length=50, blank=True,null=True)
    about_title = models.CharField(_('Про нас заголовок'), max_length=50, blank=True,null=True)
    about_description = RichTextField(_('Про нас текст опису'), blank=True, null=True)
    about_picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('малюнок дло блоку Про нас')
    )
    report_pdf = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_('Структура власності'),
    )
    manual_name = models.CharField(_('Налаштування приймача'), max_length=150, blank=True,null=True)
    manual_title = models.CharField(_('Заголовок блоку налаштування'), max_length=250, blank=True,null=True)
    manual_text = models.CharField(_('Текст налаштувань'), max_length=550, blank=True,null=True)
    online_name = models.CharField(_('Онлайн провайдери назва блоку'), max_length=150, blank=True,null=True)
    online_title = models.CharField(_('Онлайн провайдери заголовок'), max_length=250, blank=True,null=True)
    online_text = RichTextField(_('Онлайн провайдери опис'), blank=True,null=True)


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
        FieldPanel('report_pdf'),
    ]

    def get_context(self, request):
        logger.info(f'Homepage (get_context) was accessed by {request.user} ')
        context = super().get_context(request)
        now = datetime.now()
        chart_lines_today = tvweek.models.ChartLine.objects.filter(
            start_time__date=now.date(),
            start_time__gt=now
        ).select_related('project_of_program').order_by('start_time')

        # check lines
        context['chart_lines'] = [
            {
                'time': line.start_time.strftime('%H:%M'),
                'program_title': line.program_title,
                'project_title': line.project_of_program.title if line.project_of_program else None
            }
            for line in chart_lines_today
        ]

        return context