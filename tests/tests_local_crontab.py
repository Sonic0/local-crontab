import unittest

from local_crontab.converter import Converter

from fixtures.valid_crons import valid_crons_to_convert_list
from fixtures.valid_crons import valid_crons_to_convert_string


class LocalCrontabTest(unittest.TestCase):

    def test_convert_cron_to_list_of_utc_cron(self):
        for valid_cron in valid_crons_to_convert_list:
            with self.subTest(range=valid_cron):
                crontab = Converter(valid_cron.get('in'), valid_cron.get('timezone'))
                result = crontab.to_utc_crons()
                self.assertEqual(valid_cron.get('out'), result)

    def test_convert_cron_to_utc_cron(self):
        for valid_cron in valid_crons_to_convert_string:
            with self.subTest(range=valid_cron):
                crontab = Converter(valid_cron.get('in'), valid_cron.get('timezone'))
                result = crontab.to_utc_cron()
                self.assertEqual(valid_cron.get('out'), result)
