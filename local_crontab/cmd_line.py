try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata
import click

from local_crontab.converter import Converter


@click.command()
@click.option("--timezone", "-t", type=str, default=None, help="The timezone to use. Defaults to system timezone")
@click.option("--shift", "-s", is_flag=True, default=False, help="Shift Cron string, hour and day, to utc. "
                                                              "Pay attention, conversion non valid for many cases")
@click.version_option(metadata.version('local-crontab'))
@click.argument('crontab', required=True)
def main(crontab, timezone, shift,):
    """
    Convert a crontab, in a localized timezone, into a set of UTC crontabs.
    """
    if not timezone:
        click.secho("Timezone not provided, it will be used your local timezone", fg="yellow")
    converter = Converter(crontab, timezone)
    if not shift:
        converted_crontabs = converter.to_utc_crons()
        for crontab in converted_crontabs:
            click.secho(message=crontab, nl=True, bold=True, fg='cyan')
    else:
        converted_crontab = converter.to_utc_cron()
        click.secho(message=converted_crontab, nl=True, bold=True, fg='cyan')


if __name__ == "__main__":
    main()
