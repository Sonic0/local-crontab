valid_crons_to_convert = [
    {
        'in': '5 1 * 7-8 *',
        'timezone': 'Europe/Rome',
        'out': ['5 23 30 6 *', '5 23 * 7 *', '5 23 1-30 8 *']
    },
    {
        'in': '5 1 * 4-5 *',
        'timezone': 'Europe/Rome',
        'out': ['5 23 31 3 *', '5 23 * 4 *', '5 23 1-30 5 *']
    },
    {
        'in': '0 0 1 JAN SUN',
        'timezone': 'Europe/Rome',
        'out': ['0 23 31 12 0']
    },
    {
        'in': '5 * * 4-5 *',
        'timezone': 'Europe/Rome',
        'out': ['5 * * 4-5 *']
    },
]
