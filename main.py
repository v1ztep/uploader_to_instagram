import requests
import os
import urllib3


def download_image(url, image_name, dest_folder='images'):
    response = get_response(url)

    os.makedirs(dest_folder, exist_ok=True)
    with open(f'{dest_folder}/{image_name}', 'wb') as file:
        file.write(response.content)


def get_response(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    if response.ok:
        return response
    raise requests.HTTPError


def fetch_spacex_last_launch():
    response_spacex = get_response('https://api.spacexdata.com/v4/launches'
                                   '/latest')

    spacex_images = response_spacex.json()
    image_links = spacex_images['links']['flickr']['original']

    for numb, image_url in enumerate(image_links, 1):
        image_name = f'spacex{numb}.jpg'
        download_image(image_url, image_name)


def get_extension(url):
    url_split = url.split('.')
    return url_split[-1]


def fetch_image_hubble(image_id):
    response_hubble = get_response(
        f'http://hubblesite.org/api/v3/image/{image_id}')

    hubble_images = response_hubble.json()
    image_links = hubble_images['image_files']

    last_image = image_links[-1]
    image_url = last_image['file_url'].replace('//', 'https://')
    extension = get_extension(image_url)
    image_name = f'{image_id}.{extension}'
    download_image(image_url, image_name)


def main():
    # fetch_spacex_last_launch()

    fetch_image_hubble(1)


if __name__ == '__main__':
    main()
