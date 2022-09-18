import json
import requests

def get_data_response(url, key):
    request = requests.get(url)
    response = request.json()
    return response[key]

def download_symbology_icons(data):
    for element in data:
        img_data = requests.get(element['svg_uri']).content
        split = element['svg_uri'].split('/')
        file_name = split[-1][0:split[-1].index('.')]
        with open(f'./images/symbols/{file_name}.svg','wb') as f:
            f.write(img_data)

def get_all_available_sets_from_json():
    sets = []
    with open('downloads/Default Cards.json', 'r', encoding='utf8') as f:
        json_file = json.load(f)
        for element in json_file:
            try:
                if element['set']:
                    if element['set'] not in sets:
                        sets.append(element['set'])
            except Exception:
                pass
        return sets

def download_sets_icons(sets):
    for element in sets:
        data = get_data_response(f'https://api.scryfall.com/sets/{element}', 'icon_svg_uri')
        img_data = requests.get(data).content
        split = data.split('/')
        file_name = split[-1][0:split[-1].index('.')]
        with open(f'./images/sets/{file_name}.svg','wb') as f:
            f.write(img_data)

def download_all_icons():
    data = get_data_response('https://api.scryfall.com/symbology', 'data')
    download_symbology_icons(data)

    sets = get_all_available_sets_from_json()
    download_sets_icons(sets)

#DEBUG
#download_all_icons()