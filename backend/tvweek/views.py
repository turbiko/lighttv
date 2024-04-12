from datetime import datetime
import datetime as dt
import pandas as pd

from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from project.models import Project
from .forms import TVChartUploadForm
from .models import ChartLine
from .tools import get_date_from_cell_0, generate_week_dict


def upload_chart(request):

    TAB_NAME_IN_XLS = 'Укр'  # TODO: it was hardcoded, refactor it
    tv_chart_file = ''
    selected_date = ""  # reset once before load file, continuous value for chart line date control

    if request.method == 'POST':
        form = TVChartUploadForm(request.POST, request.FILES)
        past_time = False
        if form.is_valid():
            tv_chart_file = form.cleaned_data['tv_chart_file']
            df = pd.read_excel(tv_chart_file, header=0, sheet_name=TAB_NAME_IN_XLS)

            for index, row in df.iterrows():
                if isinstance(row.iloc[0], str):  # week day title - take chart_line date value
                    past_time = False  # for new day reset next day checker
                    string_dict_date = get_date_from_cell_0(row.iloc[0])
                    selected_date = datetime.strptime(string_dict_date['date_str'].strip(), '%d.%m.%Y').date()
                    continue
                if isinstance(row.iloc[0], dt.time):
                    if not past_time:
                        past_time = row.iloc[0]
                    elif past_time < row.iloc[0]:
                        past_time = row.iloc[0]
                    elif past_time > row.iloc[0]:
                        past_time = row.iloc[0]
                        selected_date += dt.timedelta(days=1)

                    if pd.isnull(row.iloc[1]) and pd.isnull(row.iloc[2]):  # when time exist but other data not exist
                        continue

                    # looking for related project for chart_line title
                    related_projects = Project.objects.filter(chart_name_short__icontains=row.iloc[1].strip())
                    projects_count = related_projects.count()
                    chart_line_project_of_program = None  # reset value before checking
                    if projects_count > 1:
                        for project in related_projects:
                            if project.chart_name_short in chart_line.program_title:
                                chart_line_project_of_program = project
                                break
                    elif projects_count == 1:  # if program name exact matches
                        chart_line_project_of_program = related_projects.first()

                    # finalize process by saving chart_line model element
                    chart_line_weekday = selected_date.weekday()

                    chart_line_date = datetime.combine(selected_date,row.iloc[0])
                    chart_line, _temp = ChartLine.objects.update_or_create(
                        start_time=chart_line_date,
                        day_of_week=chart_line_weekday,
                        program_title=row.iloc[1].strip(),
                        program_genre=row.iloc[2].strip() if pd.notnull(row.iloc[2]) else '',
                        project_of_program=chart_line_project_of_program
                    )
                    # chart_line.save() # ChartLine.objects.update_or_create make it automatically
    else:
        form = TVChartUploadForm()
    messages.success(request, 'TV Chart data uploaded successfully.')

    # clear chart_line table from old elements
    threshold_date = dt.datetime.now() - dt.timedelta(days=60)  #TODO: hardcoded move to site settings
    ChartLine.objects.filter(start_time__lt=threshold_date).delete()
    return render(request, 'tvweek/upload_chart.html', {'form': form})


def chart_page(request):
    context = {}
    now_day_is = datetime.datetime.now()
    # week days dict {week_day_name: Пн Вт Ср Чт Пт Сб Нд, detestamp}
    week_days = generate_week_dict(now_day_is)
    context['week_days'] = week_days
    return render(request, 'tvweek/week_chart.html', context)
