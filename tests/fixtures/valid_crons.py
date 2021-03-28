valid_crons_to_convert_list = [
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

valid_crons_to_convert_string = [
    {
        'in': '5 21-23 20-25 7-8 *',
        'timezone': 'Etc/GMT',  # Etc/GMT-0
        'out': '5 21-23 20-25 7-8 *'
    },
    {
        'in': '* 23 3 * *',
        'timezone': 'America/New_York',
        'out': '* 3 4 * *'
    },
    {
        'in': '5 21-23 20-25 7-8 *',
        'timezone': 'America/New_York',
        'out': '5 1-3 21-26 7-8 *'
    },
    {
        'in': '5 0-1 20-25 7-8 *',
        'timezone': 'Europe/Rome',
        'out': '5 22-23 19-24 7-8 *'
    },
    {
        'in': '5 0-3 * 7-8 *',
        'timezone': 'Europe/Rome',
        'out': '5 0-1,22-23 * 7-8 *'
    },
    # {
    #     'in': '5 0-4 3-5 7-8 *',
    #     'timezone': 'Europe/Rome',
    #     'out': ['5 22-23 2 7-8 *', '5 0-2,22-23 3-4 7-8 *', '5 0-2 5 7-8 *']
    # },
]
