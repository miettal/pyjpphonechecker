import click

from . import checker
from pprint import pprint as pp


@click.command
@click.argument('phone-number')
def main(phone_number):
    r = checker.telenavi(phone_number)
    pp(r)
    r = checker.jpnumber(phone_number, headless=True)
    pp(r)


if __name__ == '__main__':
    main()
