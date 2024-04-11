import os
import logging
from datetime import datetime
import datetime as dt
import pandas as pd
import re

from django.utils import timezone
from django.db.models import F
from django.db.models.functions import ExtractWeek, ExtractYear
from django.utils.translation import gettext_lazy as _
from django.db import models
from wagtail.models import Page
from .tools import get_current_week_range

class ChartLine(models.Model):
    day_of_week = models.IntegerField(_("День тижня (1-Пн,7-Нд"), blank=True, null=True)
    start_time = models.DateTimeField(_("Час початку"), blank=True, null=True) #  datetime when program started
    program_title = models.CharField(_("Назва програми"), max_length=200)
    program_genre = models.CharField(_("Жанр програми"), max_length=100, blank=True, null=True)
    project_of_program = models.ForeignKey('project.Project', blank=True, on_delete=models.SET_NULL, null=True)


def get_today_week():
    now = datetime.now()
    day_of_week = now.weekday()
    week_number = now.isocalendar().week
    year = now.year
    return {"year": year, "week_number":week_number, "day_of_week":day_of_week}


class TVChart(models.Model):
    tv_chart_file = models.FileField(max_length=255)


class WeekChart(Page):
    template = 'tvweek' + os.sep + 'week_chart.html'
    parent_page_types = ['home.HomePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        now = datetime.now()
        day_of_week = now.weekday()
        week_number = now.isocalendar().week
        year = now.year

        start_week, end_week = get_current_week_range()
        chart_lines = ChartLine.objects.filter(start_time__date__range=(start_week, end_week))
        context['chart_lines'] = chart_lines
        print(f"{chart_lines=}")
        return context

    def get_day_chart(self, day_date: datetime.date):
        ...
