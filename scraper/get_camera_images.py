import requests
import csv


domain = 'https://www.digicamdb.com/'


# STORE BRANDNAME AND URL INTO A DICT FROM CSV
model_image_urls = []

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
            model_image_urls.append(row[6])

print(model_image_urls)


for i in range(100):
    image_url = domain+model_image_urls[i]
    image_name = model_image_urls[i].split('/')[-1]
    print(image_name)
    img_data = requests.get(image_url).content
    with open('./images/'+image_name, 'wb') as handler:
        handler.write(img_data)
