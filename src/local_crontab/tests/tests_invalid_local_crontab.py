import unittest

from local_crontab.local_crontab import Converter

from fixtures.invalid_crons import invalid_crons_to_convert


class LocalCrontabInvalidTest(unittest.TestCase):

    def test_convert_cron_to_utc(self):
        for invalid_cron in invalid_crons_to_convert:
            with self.subTest(range=invalid_cron):
                with self.assertRaises(invalid_cron['error'], msg=invalid_cron['message']):
                    crontab = Converter(invalid_cron.get('in'), invalid_cron.get('timezone'))
                    crontab.to_utc_crons()
