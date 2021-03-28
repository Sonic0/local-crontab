from typing import Optional, List

from cron_converter import Cron
from datetime import datetime, timezone
from dateutil import tz
from calendar import monthrange

CronConverterNestedLists = List[List[List[int]]]


class WrongTimezoneError(Exception):
    """Error Should be raised when an unexpected timezone is detected as input"""
    pass


class Converter:
    """Creates an instance of Converter.

    Converter objects is a converter from local to UTC date time.

    Attributes:
        cron_string (str): The cron string to convert.
        timezone (str): The timezone as string. eg -> 'Europe/Rome'
        year (int): The year crontab will be applied in
    """
    def __init__(self, cron_string: str, timezone_str: Optional[str] = None, year: Optional[int] = None):
        self.localized_cron = Cron(cron_string)
        self.localized_cron_list = self.localized_cron.to_list()
        if not timezone_str:
            self.timezone = tz.tzlocal()  # Use current Local Timezone if no input timezone
        elif tz.gettz(timezone_str):
            self.timezone = tz.gettz(timezone_str)
        else:
            raise WrongTimezoneError("Incorrect Timezone string")
        self.cron_year = year if bool(year) else datetime.now(tz=self.timezone).year

    def to_utc_cron(self) -> str:
        """Function to convert a localized cron string to UTC cron string.
        This function converts only hour and day part, however the result in not reliable in some cases due to not handled DST.

        :return: cron_string (str): the resulting cron readable by all systems.
        """
        # If the hour part of Cron is the entire range of hours (*) is useless proceed
        if self.localized_cron.parts[1].is_full():
            return self.localized_cron.to_string()
        # Get offset from utc in hours
        local_offset = self.timezone.utcoffset(datetime.now(self.timezone))
        local_offset_hours = int(local_offset.total_seconds() / 3600)  # offset in second / second in an hour

        utc_cron_list = self.localized_cron_list
        day_shift = (False, 0)
        hour_shifted_count = 0
        # Hours shift
        hour_range = self.localized_cron.parts[1].possible_values()  # Range of hours that a Cron hour object Part can assume
        cron_hours_part_utc = [hour - local_offset_hours for hour in self.localized_cron_list[1]]  # Shift hour based of offset from UTC
        for idx, hour in enumerate(cron_hours_part_utc):
            if hour < hour_range[0]:
                # Hour < 0 (ex: -2, -1) as intended in the previous day, so shift them to a real hour (ex: 22, 23)
                day_shift = (True, -1)
                hour += len(hour_range)  # Convert negative hour to real (ex: -2 + 24 = 22, -1 + 24 = 23)
                cron_hours_part_utc.pop(idx)
                cron_hours_part_utc.insert(idx, hour)
                hour_shifted_count += 1
            elif hour > hour_range[-1]:
                # Hour < 0 (ex: -2, -1) as intended in the previous day, so shift them to a real hour (ex: 22, 23)
                day_shift = (True, 1)
                hour -= len(hour_range)  # Convert not existing hour to real (ex: 25 - 24 = 1, 26 - 24 = 2)
                cron_hours_part_utc.pop(idx)
                cron_hours_part_utc.insert(idx, hour)
                hour_shifted_count += 1
        utc_cron_list[1] = cron_hours_part_utc

        # Day shift
        # if it is necessary a day shift and the original days Cron Part is not full(*)
        if day_shift[0] and not self.localized_cron.parts[2].is_full():
            # All hours shifted to the a next or previous day
            if day_shift[0] and hour_shifted_count == len(cron_hours_part_utc):
                utc_cron_list[2] = [day + day_shift[1] for day in self.localized_cron_list[2]]
            # Only one or more hours shifted to the a next or previous day
            elif day_shift[0] and hour_shifted_count != len(cron_hours_part_utc):
                raise ValueError("Operation cross days not supported. Sorry! (╥﹏╥)")

        utc_cron = Cron()
        utc_cron.from_list(utc_cron_list)

        return utc_cron.to_string()

    def to_utc_crons(self) -> List[str]:
        """The main function to convert the cron string to a list of UTC cron strings.

        :return: cron_strings (list of str): the resulting cron list readable by all systems.
        """
        # If the hour part of Cron is the entire range of hours (*) is useless proceed
        cron_hour_part = self.localized_cron.parts[1]
        if cron_hour_part.is_full():
            return [self.localized_cron.to_string()]

        # Create the nested list with every single day belonging to the cron
        utc_list_crontabs = self._day_cron_list()
        # Group hours together
        utc_list_crontabs = self._group_hours(utc_list_crontabs)
        # Group days together
        utc_list_crontabs = self._group_days(utc_list_crontabs)
        # Convert a day-full month in *
        utc_list_crontabs = self._range_to_full_month(utc_list_crontabs)
        # Group months together by hour / minute & days
        utc_list_crontabs = self._group_months(utc_list_crontabs)

        cron_strings = []
        for cron_list in utc_list_crontabs:
            cron = Cron()
            cron.from_list(cron_list)
            cron_strings.append(cron.to_string())

        return cron_strings

    def _day_cron_list(self) -> CronConverterNestedLists:
        """Returns a nested list struct in which each element represents every single day in cron list format,
        readable by Cron-Converter Object.
        Sometimes days included in the cron range do not exist in the real life for every month(example: February 30),
        so these days will be discarded.

        :return: acc (list of ints): nested list made up of cron lists readable by Cron-Converter Object.
        """
        utc_list_crontabs = list()
        for month in self.localized_cron_list[3]:
            for day in self.localized_cron_list[2]:
                for hour in self.localized_cron_list[1]:
                    try:
                        local_date = datetime(self.cron_year, month, day, hour, 0, tzinfo=self.timezone)
                    except ValueError:
                        continue  # skip days that not exist (eg: 30 February)
                    utc_date = (local_date - local_date.utcoffset()).replace(tzinfo=timezone.utc)
                    # Create one Cron list for each hour
                    utc_list_crontabs.append([
                        [minute for minute in self.localized_cron_list[0]],
                        [utc_date.hour],
                        [utc_date.day], [utc_date.month], self.localized_cron_list[4]])
        return utc_list_crontabs

    def _range_to_full_month(self, utc_list_crontabs: CronConverterNestedLists) -> CronConverterNestedLists:
        """Returns a modified list with the character '*' as month in case of the month is day-full.
        The Cron-Converter read a full month only if it has 31 days.

        :return: acc (nested list of ints): modified nested list made up of cron lists readable by Cron-Converter Object.
        """
        acc = []
        for element in utc_list_crontabs:
            if len(element[2]) == monthrange(self.cron_year, element[3][0])[1]:
                element[2] = [day for day in range(1, 32)]

            acc.append(element)
        return acc

    @staticmethod
    def _group_hours(utc_list_crontabs: CronConverterNestedLists) -> CronConverterNestedLists:
        """Group hours together by minute, day and month.

        :param utc_list_crontabs: Nested list of crontabs not grouped.
        :return: acc (nested list of ints): filtered nested list made up of cron lists readable by Cron-Converter Object.
        """
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

    @staticmethod
    def _group_days(utc_list_crontabs: CronConverterNestedLists) -> CronConverterNestedLists:
        """Group days together by hour, minute and month.

        :param utc_list_crontabs: Nested list of crontabs previously grouped in hours.
        :return: acc (nested list of ints): filtered nested list made up of cron lists readable by Cron-Converter Object.
        """
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

    @staticmethod
    def _group_months(utc_list_crontabs: CronConverterNestedLists) -> CronConverterNestedLists:
        """Group months together by minute, days and hours

        :param utc_list_crontabs: Nested list of crontabs previously grouped in days.
        :return: acc (nested list of ints): filtered nested list made up of cron lists readable by Cron-Converter Object.
        """
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

    # TODO next release
    # @staticmethod
    # def _combine_month(utc_list_crontabs: CronConverterNestedLists) -> CronConverterNestedLists:
    #     """Combine start & end of year if possible.
    #
    #     :param utc_list_crontabs: Nested list of crontabs previously grouped in months.
    #     :return: acc (nested list of ints): filtered nested list made up of cron lists readable by Cron-Converter Object.
    #     """
    #     if len(utc_list_crontabs) > 1 and \
    #             utc_list_crontabs[0][0] == utc_list_crontabs[-1][0] and \
    #             utc_list_crontabs[0][1] == utc_list_crontabs[-1][1]:
    #         utc_list_crontabs[0][3].append(utc_list_crontabs.pop()[3][0])
    #     return utc_list_crontabs
