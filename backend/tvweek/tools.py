import pytz
from datetime import datetime, timedelta
import locale

# встановити українську локаль = працює але проблеми з кодуванням
try:
    locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
except locale.Error:
    print("Українська локаль не підтримується на цій системі.")


def get_date_from_cell_0(cell_data: str) -> dict:
    """
       input:  'Понеділок, 08.04.2024'
       output: {'day_name':'Понеділок', 'date_str':'08.04.2024' }
    """
    if type(cell_data) == str:
        day_name, date_str = cell_data.split(',')
    return {'day_name': day_name, 'date_str': date_str}


def get_current_week_range(current_date: datetime.date):
    my_today = current_date
    # (0=Monday, 6=Sunday)
    my_weekday = my_today.weekday()
    my_start_week = my_today - timedelta(days=my_weekday)  # Monday
    my_end_week = my_start_week + timedelta(days=6)  # Sunday
    return my_start_week, my_end_week, my_weekday


def generate_week_dict(current_chart_date):
    start_week, end_week, today_weekday = get_current_week_range(current_chart_date)
    days_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    days_info = []
    current_date = start_week

    while current_date <= end_week:
        print(f'{current_date=} {current_date.weekday()=}')
        day_info = {
            'day_name': days_names[current_date.weekday()],
            'day_date': current_date.strftime("%d %B"),  # Форматування дати українською мовою
            'weekday_number': current_date.weekday(),
            'full_date': current_date.isoformat(),  # Дата у форматі YYYY-MM-DD
            'is_today': int(current_date == datetime.now(pytz.timezone("Europe/Kiev")).date())
        }
        days_info.append(day_info)
        current_date += timedelta(days=1)  # наступний день

    return days_info


if __name__ == "__main__":
    my_timezone = pytz.timezone("Europe/Kiev")  # Заданий часовий пояс "Europe/Kiev"
    print(f"{get_date_from_cell_0('Понеділок, 08.04.2024')=}")
    start_week, end_week, weekday = get_current_week_range(datetime.now().date())
    print(f"{start_week=} {end_week=} {weekday=}")
    print(f"{get_current_week_range(datetime.now().date())=}")
    days_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    print(f"{generate_week_dict(datetime.now().date())=}")
