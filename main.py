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
    image_links = spacex_dict['links']['flickr']['original']

    for numb, image_url in enumerate(image_links, 1):
        image_name = f'spacex{numb}.jpg'
        download_image(image_url, image_name)


def get_extension(url):
    url_split = url.split('.')
    return url_split[-1]


def main():
    # fetch_spacex_last_launch()

    response_hubble = get_response('http://hubblesite.org/api/v3/image/1')

    hubble_dict = response_hubble.json()
    image_links = hubble_dict['image_files']

    for dict in image_links:
        image_url = dict['file_url'].replace('//', 'https://')
        print(get_extension(image_url))


if __name__ == '__main__':
    main()
