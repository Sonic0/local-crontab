import unittest

from local_crontab import Converter


class LocalCrontabTest(unittest.TestCase):

    def test_utc(self):
        crontab = Converter('5 1 * 1-10 *', 'Europe/Rme')
        result = crontab.utc_cron()
        self.assertEqual(['5 1 * 1 *', '5 1 * 2 *', '5 1 1-27 3 *', '5 2 28-31 3 *', '5 2 * 4 *', '5 2 * 5 *',
                          '5 2 * 6 *', '5 2 * 7-8 *', '5 2 1-30 9-10 *', '5 1 31 10 *'], result)
