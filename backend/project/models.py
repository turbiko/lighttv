import os
import logging
from datetime import datetime
import datetime as dt
from django.db import models
from django.db.models import Count
from django.utils.translation import activate, gettext_lazy as _, get_language
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import InlinePanel, PageChooserPanel, FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField


logger = logging.getLogger('svitlo')


class Genre(models.Model):
    name = models.CharField(_('Назва жанру'),max_length=100)
    description = models.TextField(_('Опис жанру'), blank=True, null=True)

    def __str__(self):
        return self.name


class ProjectGenres(Orderable):
    genre = models.ForeignKey(Genre, related_name='+', null=True, on_delete=models.SET_NULL)
    page = ParentalKey('project.Project', related_name='project_genres')
    panels = [
        FieldPanel('genre'),
    ]
class ProjectType(models.Model):
    name = models.CharField(_('Тип проєкту'), max_length=255)

    def __str__(self):
        return self.name


class Project(Page):
    template = 'project' + os.sep + 'project-page.html'
    parent_page_types = ['Projects_List']
    date_production = models.DateField(_('Дата релізу'), blank=True, null=True)  # TODO: use YEAR only
    chart_name_short = models.CharField(_('Коротка назва для тв-програми'), max_length=30,blank=True, null=True)
    duration_minutes = models.IntegerField(_('Хронометраж, хв.'), blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, null=True, on_delete=models.SET_NULL)
    image_slider_big = models.ForeignKey(  # post image big slider
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    image_slider_mobile = models.ForeignKey(  # post image mobile slider
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    feed_image = models.ForeignKey(  # preview image
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    description_short = models.TextField(null=True, blank=True,)
    description = RichTextField(null=True, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('date_production'),
        FieldPanel('chart_name_short'),
        FieldPanel('duration_minutes'),
        FieldPanel('project_type'),
        FieldPanel('image_slider_big'),
        FieldPanel('image_slider_mobile'),
        FieldPanel('feed_image'),
        FieldPanel('description_short'),
        FieldPanel('description'),
        MultiFieldPanel(
                [InlinePanel("project_genres", label=_("Жанр"))],
                heading=_("Додаткова інформація"),
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        if self.project_type:
            # Exclude the current project from the queryset
            similar_projects = Project.objects.live().filter(project_type=self.project_type).exclude(pk=self.pk)
            context['similar_projects'] = similar_projects
            for pr1 in similar_projects:
                print(f"{pr1.feed_image}")

        return context


class Projects_List(Page):  # noqa
    template = 'project' + os.sep + 'projects-list.html'
    subpage_types = ['Project']
    parent_page_types = ['home.HomePage']
    page_description = _("Сторінка проєктів")

    @classmethod
    def accessible(cls, request):  # Projects_List
        """
        you can use it for filtering projects for visitors there if you need
        as example may use b2b project as reference
        :param request:
        :return: all active pages
        """

        active_projects = Project.objects.live()  # .order_by('top_priority')
        # active_projects = Project.objects.live().filter(locale=Locale.get_active())
        for project in active_projects:
            print(f'{project.project_type=}, {project.title=}')

        logger.debug(f'Projects (accessible) for {request.user} {active_projects.count()=}')
        return active_projects

    def get_context(self, request):  # Projects_List
        context = super().get_context(request)
        # Get projects accessible for user
        # all_projects = self.accessible(request=request)
        project_types = ProjectType.objects.annotate(num_projects=Count('project')).filter(num_projects__gt=0)
        projects = Project.objects.live()
        logger.debug(f'Projects (get_context) for {request.user} {projects.count()=}')

        # Filter projects by project type if 'type' GET parameter is set
        project_type_id = request.GET.get('type')
        if project_type_id:
            projects = projects.filter(project_type_id=project_type_id)

        context['project_types'] = project_types
        context['projects'] = projects
        return context

