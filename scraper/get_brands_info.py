from requests_html import HTMLSession
import csv
import base64
import requests


session = HTMLSession()

domain = 'https://www.digicamdb.com/'
brands_url = '/cameras'


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)


with open('brands.csv', mode='w') as brands_file:
    fieldnames = ['brand_name',  'brand_url',
                  'hq_country', 'num_of_cameras', 'brand_logo_url', 'brand_logo_base64']
    writer = csv.DictWriter(
        brands_file, fieldnames=fieldnames)
    writer.writeheader()

    r = session.get(domain+brands_url, verify=False)
    r.html.render()
    brand_items = r.html.find('.brd_inner')

    for item in brand_items:
        new_row = {}

        brand_div = item.find('.brd_inner_div', first=True)
        brand_a = brand_div.find('a', first=True)
        new_row['brand_url'] = brand_a.attrs['href']

        brand_logo_url = brand_a.find('img', first=True).attrs['src']
        new_row['brand_logo_url'] = brand_logo_url

        new_row['brand_logo_base64'] = get_as_base64(domain+brand_logo_url)

        brand_name = brand_a.find('img', first=True).attrs['alt'].split()[0]
        new_row['brand_name'] = brand_name

        brand_info = item.find('.font_tiny', first=True).find('b')
        new_row['hq_country'] = brand_info[0].text
        new_row['num_of_cameras'] = brand_info[1].text

        print(new_row)
        writer.writerow(new_row)
        # print(get_as_base64(logo_url))
