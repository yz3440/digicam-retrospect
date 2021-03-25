import requests
from requests_html import HTMLSession
import csv
import base64


session = HTMLSession()

domain = 'https://www.digicamdb.com/'


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)


# STORE BRANDNAME AND URL INTO A DICT FROM CSV
model_url = {}

with open('camera_urls.csv') as brands_file:
    fieldnames = ['brand_name',  'model_name',
                  'year', 'megapixels', 'sensor_size', 'model_url', 'model_image_url', 'model_image_base64']
    brands_reader = csv.reader(brands_file, delimiter=',')
    line_count = 0
    for row in brands_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            model_url[row[1]] = row[5]

print(model_url)


def get_model_details_from_html(html, model_name):
    row = {}
    spec_table = html.find('.table_specs', first=True).find('tr')
    for table_row in spec_table:
        spec_name = table_row.find('td')[0].text[:-1]
        spec_value = table_row.find('td')[1].text

        # Handle Legend for Yes / No
        if(table_row.find('td')[1].find('span', first=True)):
            if table_row.find('td')[1].find('span', first=True).attrs['class'][0] == 'yes':
                spec_value = 'Yes'
            elif table_row.find('td')[1].find('span', first=True).attrs['class'][0] == 'no':
                spec_value = 'No'

        if spec_name == 'Depth of field':
            continue
        if spec_name == 'Megapixels':
            spec_name = 'Total megapixels'
        row[spec_name] = spec_value

    row['Image'] = domain+html.find('.camera_image_single', first=True).find(
        'img', first=True).attrs['src']
    return row


with open('camera_details.csv', mode='w') as camera_details_file:
    fieldnames = ['Brand', 'Model', 'Also known as', 'Effective megapixels', 'Total megapixels', 'Sensor size', 'Sensor type', 'Sensor resolution', 'Max. image resolution', 'Crop factor', 'Optical zoom', 'Digital zoom', 'ISO', 'RAW support', 'Manual focus', 'Normal focus range', 'Macro focus range',
                  'Focal length (35mm equiv.)', 'Aperture priority', 'Max aperture', 'Max. aperture (35mm equiv.)', 'Metering', 'Exposure Compensation', 'Shutter priority', 'Min. shutter speed', 'Max. shutter speed', 'Built-in flash', 'External flash', 'Viewfinder', 'White balance presets', 'Screen size', 'Screen resolution', 'Video capture', 'Max. video resolution', 'Storage types', 'USB', 'HDMI', 'Wireless', 'GPS', 'Battery', 'Weight', 'Dimensions', 'Year', 'Image']
    writer = csv.DictWriter(
        camera_details_file, fieldnames=fieldnames)
    writer.writeheader()

    for model_name, model_url in model_url.items():
        r = session.get(domain+model_url, verify=False)
        # r.html.render()

        print(model_name, domain+model_url)
        row = get_model_details_from_html(r.html, model_name)
        writer.writerow(row)
