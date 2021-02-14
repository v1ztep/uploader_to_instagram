import requests
import os


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


def fetch_spacex_last_launch():
    response_spacex = get_response('https://api.spacexdata.com/v4/launches'
                                   '/latest')

    spacex_dict = response_spacex.json()
    spacex_links = spacex_dict['links']['flickr']['original']

    for numb, image_url in enumerate(spacex_links, 1):
        image_name = f'spacex{numb}.jpg'
        download_image(image_url, image_name)


def main():
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
