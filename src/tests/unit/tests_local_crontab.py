import unittest

from local_crontab import Converter


class LocalCrontabTest(unittest.TestCase):

    def test_utc(self):
        crontab = Converter('5 1 * 1-10 *', 'Europe/Rome')
        result = crontab.to_utc_crons()
        self.assertEqual(['5 0 * 1-2 *',
                          '5 0 1-27 3 *',
                          '5 23 28-31 3 *',
                          '5 23 * 4-9 *',
                          '5 23 1-30 10 *',
                          '5 0 31 10 *'], result)
