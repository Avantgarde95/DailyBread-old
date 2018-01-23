import datetime
import calendar

calendar.setfirstweekday(calendar.SUNDAY)
offset_utc = datetime.timedelta(hours=9)


class Timetools(object):
    @staticmethod
    def get_today():
        date = datetime.datetime.utcnow() + offset_utc
        return date.year, date.month, date.day

    @staticmethod
    def get_weekday(year, month, day):
        return (calendar.weekday(year, month, day) + 1) % 7

    @staticmethod
    def get_calendar(year, month):
        table_calendar = calendar.monthcalendar(year, month)
        num_weeks = len(table_calendar)

        if num_weeks == 5:
            return table_calendar + [[0] * 7]
        elif num_weeks == 4:
            return [[0] * 7] + table_calendar + [[0] * 7]
        else:
            return table_calendar

    @staticmethod
    def get_diffdays(year_start, month_start, day_start,
                     year_end, month_end, day_end):
        date_start = datetime.date(year_start, month_start, day_start)
        date_end = datetime.date(year_end, month_end, day_end)
        return (date_end - date_start).days
