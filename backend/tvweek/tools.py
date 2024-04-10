from datetime import datetime, timedelta
from django.utils import timezone

def get_date_from_cell_0(cell_data:str)->dict:
    """
       input:  'Понеділок, 08.04.2024'
       output: {'day_name':'Понеділок', 'date_str':'08.04.2024' }
    """
    if type(cell_data) == str:
        day_name, date_str = cell_data.split(',')
    return {'day_name': day_name, 'date_str': date_str }


def get_current_week_range():
    today = timezone.now().date()
    # (0=Monday, 6=Sunday)
    weekday = today.weekday()
    start_week = today - timedelta(days=weekday)  # Monday
    end_week = start_week + timedelta(days=6)  # sunday
    return start_week, end_week
