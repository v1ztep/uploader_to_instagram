import requests
import os
import json


def download_image(url, image_name, dest_folder='images'):
    response = get_response(url)

    os.makedirs(dest_folder, exist_ok=True)
    with open(f'{dest_folder}/{image_name}', 'wb') as file:
        file.write(response.content)


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    if response.ok:
        return response
    raise requests.HTTPError


def main():
    # url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    # image_name = 'hubble.jpeg'
    #
    # download_image(url, image_name)

    response_spacex = get_response('https://api.spacexdata.com/v4/launches'
                                   '/latest')

    # with open('images/spacex_response.json', "w", encoding='utf8') as file:
    #     json.dump(response_spacex.json(), file, ensure_ascii=False, indent=4)

    spacex_dict = response_spacex.json()
    spacex_links = spacex_dict['links']['flickr']['original']
    print(spacex_links)


if __name__ == '__main__':
    main()
