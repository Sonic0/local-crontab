from local_crontab.local_crontab import WrongTimezoneError

invalid_crons_to_convert = [
    {
        'in': '0 0 1 JAN SUN',
        'timezone': 'Europe/Rom',
        'error': WrongTimezoneError,
        'message': 'Invalid Timezone'
    },
]
