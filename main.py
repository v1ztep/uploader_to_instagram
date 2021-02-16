import requests
from pathlib import Path
import urllib3
from PIL import Image


def download_image(url, image_name, dest_folder='images'):
    response = get_response(url)

    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    image_path = Path(f'{dest_folder}/{image_name}')
    with open(image_path, 'wb') as file:
        file.write(response.content)


def resize_image(dest_folder):
    images_paths = list(Path(dest_folder).glob('*'))
    if images_paths:
        for img_path in images_paths:
            image = Image.open(img_path)
            width, height = image.size

            if width > 1080 or height > 1080:
                image.thumbnail((1080, 1080))

            Path(img_path).unlink()
            image.save(Path(img_path.parent,f'{img_path.stem}.jpg'))


def get_extension(url):
    url_split = url.split('.')
    return url_split[-1]


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


def get_hubble_image_ids(collection_name):
    response = get_response(
        'http://hubblesite.org/api/v3'
        f'/images?page=all&collection_name={collection_name}')
    collection = response.json()

    image_ids = []
    for image in collection:
        image_ids.append(image['id'])
    return image_ids


def main():
    # fetch_spacex_last_launch()

    # hubble_images_ids = get_hubble_image_ids('stsci_gallery')
    # for image_id in hubble_images_ids:
    #     fetch_image_hubble(image_id)
    resize_image('images')


if __name__ == '__main__':
    main()
