import re
from pprint import pprint as pp
import time

import requests

from bs4 import BeautifulSoup

from playwright.sync_api import Playwright
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


def normalize(s):
    """全角・半角などの揺れを正規化する."""
    return jaconv.normalize(jaconv.z2h(jaconv.h2z(s, kana=True, ascii=False, digit=False), kana=False, ascii=True, digit=True))


def telenavi(phone_number):
    url = f'https://www.telnavi.jp/phone/{phone_number}'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    rows = soup.select('.info_table > table > tr')

    for row in rows:
        cells = row.find_all('th') + row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            data[key] = value

    return {
        'phone_number': phone_number,
        'data': data,
        'url': url,
    }


def jpnumber(phone_number, headless=True):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context(user_agent=ua)
        page = context.new_page()
        page.goto('https://www.jpnumber.com/')
        page.get_by_placeholder('電話番号、事業者名、住所などのキーワードから検索').click()
        page.get_by_placeholder('電話番号、事業者名、住所などのキーワードから検索').fill(phone_number)
        page.locator('#DoSearch').click()
        time.sleep(0.1)
        page.get_by_role('link', name=re.compile(f'{phone_number} \\| .*')).click()
        time.sleep(0.1)
        url = page.url
        html = page.content()
        page.close()
    
        context.close()
        browser.close()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one('#result-main-right > div:nth-child(4) > div.content > table')
    rows = table.find_all('tr')
    data = {}
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            data[key] = value

    return {
        'phone_number': phone_number,
        'url': url,
        'data': data,
    }



if __name__ == '__main__':
    r = telenavi('0335814321')
    pp(r)
    r = jpnumber('0335814321', headless=False)
    pp(r)
