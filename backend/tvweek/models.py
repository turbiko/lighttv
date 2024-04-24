import os
import logging
from datetime import datetime
import datetime as dt
import pandas as pd
import re

from django.db.models.functions import ExtractWeek, ExtractYear
from django.utils.translation import gettext_lazy as _
from django.db import models
from wagtail.models import Page
from .tools import get_current_week_range, generate_week_dict


class ChartLine(models.Model):
    day_of_week = models.IntegerField(_("День тижня (1-Пн,7-Нд"), blank=True, null=True)
    start_time = models.DateTimeField(_("Час початку"), blank=True, null=True) #  datetime when program started
    program_title = models.CharField(_("Назва програми"), max_length=200)
    program_genre = models.CharField(_("Жанр програми"), max_length=100, blank=True, null=True)
    project_of_program = models.ForeignKey('project.Project', blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.start_time)


class TVChart(models.Model):
    tv_chart_file = models.FileField(max_length=255)


class WeekChart(Page):
    template = 'tvweek' + os.sep + 'week_chart.html'
    parent_page_types = ['home.HomePage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        now_day = datetime.now()
        day_of_week = now_day.weekday()
        week_number = now_day.isocalendar().week
        year = now_day.year
        # get week titles
        start_week, end_week, week_day = get_current_week_range(now_day)

        chart_lines = ChartLine.objects.filter(start_time__date__range=(start_week, end_week))

        this_week_days = [{
            'is_today': week_day_number == now_day.weekday(),
            'day_name': (start_week + dt.timedelta(days=week_day_number)).strftime('%A'),
            'day_date': (start_week + dt.timedelta(days=week_day_number)),
            'chart_lines': []
        } for week_day_number in range(7)]

        for line_temp in chart_lines:
            weekday_index = line_temp.start_time.weekday()
            this_week_days[weekday_index]['chart_lines'].append(line_temp)

        context['week_days'] = generate_week_dict(now_day)
        context['days_of'] = this_week_days

        return context

