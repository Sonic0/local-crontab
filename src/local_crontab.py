from typing import Optional, Literal

from cron_converter import Cron
from datetime import datetime, timezone
from dateutil import tz
from calendar import monthrange


class Converter:
    """
    aaa
    """
    def __init__(self, cron_string, timezone: Optional[str] = None, year: Optional[int] = None):
        self.cron = Cron(cron_string)
        self.local_list_crontab = self.cron.to_list()
        self.timezone = tz.gettz(timezone)
        self.cron_year = year if bool(year) else datetime.now(tz=self.timezone).year

    def to_utc_crons(self):
        # If the hour part of Cron is the entire range of hours (*) is useless proceed
        cron_hour_part = self.cron.parts[1]
        if cron_hour_part.is_full():
            print(self.cron.to_string())
            return self.cron.to_string()

        utc_list_crontabs = self._day_cron_list()
        # Group hours together
        utc_list_crontabs = self._group_hours(utc_list_crontabs)
        # Group days together
        utc_list_crontabs = self._group_days(utc_list_crontabs)
        # Group months together by hour / minute & days
        utc_list_crontabs = self._group_months(utc_list_crontabs)
        # Convert a day full range month in *
        utc_list_crontabs = self._range_to_full_month(utc_list_crontabs)

        cron_strings = []
        for cron_list in utc_list_crontabs:
            # Override cron object and use it to convert each crontab list
            self.cron.from_list(cron_list)
            cron_strings.append(self.cron.to_string())

        return cron_strings

    def _day_cron_list(self):
        utc_list_crontabs = list()
        for month in self.local_list_crontab[3]:
            for day in self.local_list_crontab[2]:
                for hour in self.local_list_crontab[1]:
                    try:
                        local_date = datetime(self.cron_year, month, day, hour, 0, tzinfo=self.timezone)
                    except ValueError:
                        continue  # skip days that not exist (eg: 30 February)
                    utc_date = (local_date - local_date.utcoffset()).replace(tzinfo=timezone.utc)
                    # Create one Cron list for each hour
                    utc_list_crontabs.append([
                        [minute for minute in self.local_list_crontab[0]],
                        [utc_date.hour],
                        [utc_date.day], [utc_date.month], self.local_list_crontab[4]])
        return utc_list_crontabs

    def _range_to_full_month(self, utc_list_crontabs):
        acc = []
        for element in utc_list_crontabs:
            if len(element[3]) > 1:
                full_month = False
                for element_month in element[3]:
                    last_month_day = monthrange(self.cron_year, element_month)[1]
                    if element[2][-1] == last_month_day and element[2][0] == 1:
                        full_month = True
                    else:
                        full_month = False
                if full_month:
                    element[2] = [day for day in range(1, 32)]
                    acc.append(element)
                else:
                    acc.append(element)
            else:
                last_month_day = monthrange(self.cron_year, element[3][0])[1]
                if element[2][-1] == last_month_day and element[2][0] == 1:
                    element[2] = [day for day in range(1, 32)]
                    acc.append(element)
                else:
                    acc.append(element)
        return acc

    # Group days together by minute, day and month.
    @staticmethod
    def _group_hours(utc_list_crontabs):
        acc = []
        for element in utc_list_crontabs:
            if len(acc) > 0 and \
                    acc[-1][0] == element[0] and \
                    acc[-1][2] == element[2] and \
                    acc[-1][3] == element[3]:
                acc[-1][1].append(element[1][0])
            else:
                acc.append(element)
        return acc

    # Group days together by hour, minute and month.
    @staticmethod
    def _group_days(utc_list_crontabs):
        acc = []
        for element in utc_list_crontabs:
            if len(acc) > 0 and \
                    acc[-1][0] == element[0] and \
                    acc[-1][1] == element[1] and \
                    acc[-1][3] == element[3]:
                acc[-1][2].append(element[2][0])
            else:
                acc.append(element)
        return acc

    # Group months together by minute, days and hours
    @staticmethod
    def _group_months(utc_list_crontabs):
        acc = []
        for element in utc_list_crontabs:
            if len(acc) > 0 and \
                    acc[-1][0] == element[0] and \
                    acc[-1][1] == element[1] and \
                    acc[-1][2] == element[2]:
                acc[-1][3].append(element[3][0])
            else:
                acc.append(element)
        return acc

    # combine start & end of year if possible. #TODO probably not necessary
    @staticmethod
    def _combine_month(utc_list_crontabs):
        if len(utc_list_crontabs) > 1 and \
                utc_list_crontabs[0][0] == utc_list_crontabs[-1][0] and \
                utc_list_crontabs[0][1] == utc_list_crontabs[-1][1]:
            utc_list_crontabs[0][3].append(utc_list_crontabs.pop()[3][0])
        return utc_list_crontabs
