import requests

def get_symbology_data_response(url):
    request = requests.get(url)
    response = request.json()
    return response['data']

data = get_symbology_data_response('https://api.scryfall.com/symbology')
for element in data:
    img_data = requests.get(element['svg_uri']).content
    split = element['svg_uri'].split('/')
    file_name = split[-1][0:split[-1].index('.')]
    with open(f'./images/symbols/{file_name}.svg','wb') as f:
        f.write(img_data)