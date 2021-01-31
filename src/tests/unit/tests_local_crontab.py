import unittest

from local_crontab import Converter


class LocalCrontabTest(unittest.TestCase):

    def test_utc(self):
        crontab = Converter('5 1 * 7-8 *', 'Europe/Rome')
        result = crontab.to_utc_crons()
        self.assertEqual(['5 0 * 1-2 *',
                          '5 0 1-27 3 *',
                          '5 23 28-31 3 *',
                          '5 23 * 4-9 *',
                          '5 23 1-30 10 *',
                          '5 0 31 10 *'], result)

# '5 1 * 4-5 *' --> Dato lo shift Maggio fino al 30, il 31 no perchè non abbiamo Giugno
