import requests
from requests_html import HTMLSession
import csv
import base64


session = HTMLSession()

domain = 'https://www.digicamdb.com/'


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)


# STORE BRANDNAME AND URL INTO A DICT FROM CSV
brands_name_url = {}

with open('brands.csv') as brands_file:
    fieldnames = ['brand_name',  'brand_url',
                  'hq_country', 'num_of_cameras', 'brand_logo_url', 'brand_logo_base64']
    brands_reader = csv.reader(brands_file, delimiter=',')
    line_count = 0
    for row in brands_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            brands_name_url[row[0]] = row[1]

print(brands_name_url)


def get_camera_models_from_html(html, brand_name):
    res = []
    models_items = html.find('.newest_div')
    for item in models_items:
        new_row = {}

        new_row['brand_name'] = brand_name

        model_a = item.find(
            '.newest_1', first=True).find('a', first=True)
        new_row['model_url'] = model_a.attrs['href']
        model_image_url = model_a.find('img', first=True).attrs['src']
        new_row['model_image_url'] = model_image_url
        # new_row['model_image_base64'] = get_as_base64(
        #     domain+model_image_url)

        model_div = item.find('.newest_2', first=True)
        model_info = model_div.find('div', first=True).find('b')

        new_row['model_name'] = model_info[0].text
        new_row['megapixels'] = model_info[1].text
        new_row['sensor_size'] = model_info[2].text
        new_row['year'] = model_div.find('span', first=True).text[-5:-1]
        res.append(new_row)
    print(res)
    return res


with open('camera_urls.csv', mode='w') as camera_urls_file:
    fieldnames = ['brand_name',  'model_name',
                  'year', 'megapixels', 'sensor_size', 'model_url', 'model_image_url', 'model_image_base64']
    writer = csv.DictWriter(
        camera_urls_file, fieldnames=fieldnames)
    writer.writeheader()

    for brand_name, brand_url in brands_name_url.items():
        r = session.get(domain+brand_url, verify=False)
        # r.html.render()
        max_page = int(r.html.find(
            '.browse_page', first=True).text.split()[-1])

        print(brand_name+' Page 1')
        rows = get_camera_models_from_html(r.html, brand_name)
        for row in rows:
            writer.writerow(row)

        for i in range(2, int(max_page+1)):
            print(brand_name+' Page '+str(i), domain+brand_url+str(i))
            r = session.get(domain+brand_url+str(i), verify=False)
            # r.html.render()
            rows = get_camera_models_from_html(r.html, brand_name)
            for row in rows:
                writer.writerow(row)
