from datetime import datetime
import datetime as dt
import pandas as pd

from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from project.models import Project
from .forms import TVChartUploadForm
from .models import ChartLine
from .tools import get_date_from_cell_0, generate_week_dict


def upload_chart(request):

    TAB_NAME_IN_XLS = 'Укр'  # TODO: it was hardcoded, refactor it
    tv_chart_file = ''
    selected_date = ""  # reset once before load file, continuous value for chart line date control
    chart_line = None # reset
    need_to_erase = True
    if request.method == 'POST':
        form = TVChartUploadForm(request.POST, request.FILES)
        past_time = False
        if form.is_valid():
            tv_chart_file = form.cleaned_data['tv_chart_file']
            df = pd.read_excel(tv_chart_file, header=0, sheet_name=TAB_NAME_IN_XLS)

            # looking for related project for chart_line title
            projects_set = set(Project.objects.values_list('chart_name_short', flat=True))
            print(f"upload_chart: projects short chart names {projects_set}")

            for index, row in df.iterrows():
                if isinstance(row.iloc[0], str):  # week day title - take chart_line date value
                    past_time = False  # for new day reset next day checker
                    string_dict_date = get_date_from_cell_0(row.iloc[0])
                    selected_date = datetime.strptime(
                        string_dict_date['date_str'].strip(), '%d.%m.%Y'
                        ).date()
                    # TODO: think about correct shorter chart diapason for deleting
                    if need_to_erase:  # delete all lines in future from db
                        ChartLine.objects.filter(start_time__gte=selected_date).delete()
                        need_to_erase = False
                    continue

                if isinstance(row.iloc[0], dt.time):
                    if not past_time:
                        past_time = row.iloc[0]
                    elif past_time < row.iloc[0]:
                        past_time = row.iloc[0]
                    elif past_time > row.iloc[0]:
                        past_time = row.iloc[0]
                        selected_date += dt.timedelta(days=1)
                    # when time exist but other data not exist
                    if pd.isnull(row.iloc[1]) and pd.isnull(row.iloc[2]):
                        continue

                    # finalize process by saving chart_line model element
                    chart_line_weekday = selected_date.weekday()
                    chart_line_date = datetime.combine(selected_date, row.iloc[0])

                    # get ChartLine project
                    chart_project = None
                    for chart_name in projects_set:
                        row_project_name = row.iloc[1].strip().lower()
                        if chart_name.lower() == row_project_name:  # Check for exact match
                            chart_project = Project.objects.filter(chart_name_short=chart_name).first()
                            if chart_project:  # Found project in set
                                break
                        if chart_name.lower() in row_project_name:
                            chart_project = Project.objects.filter(chart_name_short=chart_name).first()
                            if chart_project:  #  Found project in set
                                break

                    chart_line, _temp = ChartLine.objects.update_or_create(
                        start_time=chart_line_date,
                        day_of_week=chart_line_weekday,
                        program_title=row.iloc[1].strip(),
                        program_genre=row.iloc[2].strip() if pd.notnull(row.iloc[2]) else '',
                        project_of_program=chart_project
                        )

                    # chart_line.save() # ChartLine.objects.update_or_create make it automatically
    else:
        form = TVChartUploadForm()
    messages.success(request, 'TV Chart data uploaded successfully.')

    # if no errors - clear chart_line table from old elements
    threshold_date = dt.datetime.now() - dt.timedelta(days=30)  #TODO: hardcoded move to site settings
    ChartLine.objects.filter(start_time__lt=threshold_date).delete()
    return render(request, 'tvweek/upload_chart.html', {'form': form})


def chart_page(request):
    context = {}
    now_day_is = datetime.datetime.now()
    # week days dict {week_day_name: Пн Вт Ср Чт Пт Сб Нд, detestamp}
    week_days = generate_week_dict(now_day_is)
    context['week_days'] = week_days
    return render(request, 'tvweek/week_chart.html', context)


def get_current_time(request):
    current_time = timezone.now()
    return JsonResponse({'current_time': current_time.isoformat()})
