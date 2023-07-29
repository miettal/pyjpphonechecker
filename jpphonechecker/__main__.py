"""__main__."""
from pprint import pprint as pp

import click

from . import checker


@click.command
@click.argument('phone-number')
def main(phone_number):
    """電話番号を検索する."""
    r = checker.telenavi(phone_number)
    pp(r)
    r = checker.jpnumber(phone_number, headless=True)
    pp(r)


if __name__ == '__main__':
    main()
