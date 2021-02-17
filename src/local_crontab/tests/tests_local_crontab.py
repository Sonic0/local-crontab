import unittest

from local_crontab.local_crontab import Converter

from fixtures.valid_crons import valid_crons_to_convert


class LocalCrontabTest(unittest.TestCase):

    def test_convert_cron_to_utc(self):
        for valid_cron in valid_crons_to_convert:
            with self.subTest(range=valid_cron):
                crontab = Converter(valid_cron.get('in'), valid_cron.get('timezone'))
                result = crontab.to_utc_crons()
                self.assertEqual(valid_cron.get('out'), result)
